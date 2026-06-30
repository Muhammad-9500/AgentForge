import re
from dataclasses import dataclass
from typing import Callable, Optional


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    message: str


class Guardrails:
    """Deterministic input validation for AgentForge project ideas.

    This module intentionally does not use an LLM. It performs fast checks before
    user input reaches any agent, reducing the chance that prompt injection,
    unsafe software requests, executable payloads, or leaked secrets enter the
    multi-agent workflow.
    """

    MIN_LENGTH = 10
    MAX_LENGTH = 5_000
    MAX_REPEATED_CHARACTER_COUNT = 30
    MAX_NON_PRINTABLE_RATIO = 0.05

    PROMPT_INJECTION_PATTERNS = (
        r"\bignore\s+(all\s+)?(previous|prior|above)\s+(instructions?|rules?|prompts?)\b",
        r"\bdisregard\s+(all\s+)?(previous|prior|above)\s+(instructions?|rules?|prompts?)\b",
        r"\bforget\s+(all\s+)?(previous|prior|above)\s+(instructions?|rules?|prompts?)\b",
        r"\boverride\s+(the\s+)?(system|developer|assistant)\s+(instructions?|message|prompt)\b",
        r"\breveal\s+(your\s+)?(system|developer)\s+(instructions?|message|prompt)\b",
        r"\bshow\s+(me\s+)?(your\s+)?(hidden|system|developer)\s+(instructions?|message|prompt)\b",
        r"\byou\s+are\s+now\s+(in\s+)?(developer|admin|root|god)\s+mode\b",
    )

    JAILBREAK_PATTERNS = (
        r"\bjailbreak\b",
        r"\bDAN\s+mode\b",
        r"\bdo\s+anything\s+now\b",
        r"\bno\s+ethical\s+limits\b",
        r"\bwithout\s+(any\s+)?(safety|policy|ethical)\s+(rules|restrictions|limits)\b",
        r"\bbypass\s+(safety|policy|guardrails?|filters?|restrictions)\b",
    )

    DANGEROUS_REQUEST_PATTERNS = (
        r"\b(build|create|write|generate|develop|make|code|implement)\b.{0,80}\b(malware|ransomware|spyware|trojan|worm|rootkit|botnet)\b",
        r"\b(build|create|write|generate|develop|make|code|implement)\b.{0,80}\b(keylogger|credential\s+stealer|password\s+stealer|token\s+stealer)\b",
        r"\b(steal|exfiltrate|harvest|dump)\b.{0,80}\b(passwords?|credentials?|cookies?|tokens?|api\s*keys?)\b",
        r"\b(phishing|phish)\b.{0,80}\b(site|page|kit|email|login)\b",
        r"\b(ransomware|malware|spyware|keylogger)\b",
    )

    SQL_INJECTION_PATTERNS = (
        r"(?i)(\bor\b|\band\b)\s+['\"]?\d+['\"]?\s*=\s*['\"]?\d+['\"]?",
        r"(?i)union\s+select\b",
        r"(?i)(drop|alter|truncate)\s+table\b",
        r"(?i)insert\s+into\b.+\bvalues\b",
        r"(?i)update\b.+\bset\b.+\bwhere\b",
        r"(?i)delete\s+from\b.+\bwhere\b",
        r"(?i)--\s*$",
        r"(?i);\s*(drop|alter|truncate|delete|update|insert)\b",
        r"(?i)\bexec(\s|\+)+(xp_cmdshell|sp_)\b",
    )

    XSS_PATTERNS = (
        r"(?i)<\s*script\b",
        r"(?i)javascript\s*:",
        r"(?i)\bon(error|load|mouseover|focus|click)\s*=",
        r"(?i)<\s*(iframe|object|embed|svg|img)\b[^>]*(on\w+\s*=|javascript\s*:)",
        r"(?i)document\s*\.\s*(cookie|location|write)",
        r"(?i)eval\s*\(",
    )

    DANGEROUS_SHELL_PATTERNS = (
        r"(?i)\brm\s+-rf\s+(/|\*|~)",
        r"(?i)\bsudo\s+rm\s+-rf\b",
        r"(?i)\bdel\s+/[fsq]\b",
        r"(?i)\brmdir\s+/s\s+/q\b",
        r"(?i)\bformat\s+[a-z]:",
        r"(?i)\bmkfs\.",
        r"(?i)\bdd\s+if=.*\bof=/dev/",
        r"(?i)\bchmod\s+-R\s+777\b",
        r"(?i)\b(chown|chmod)\s+-R\s+.*\s+/",
        r"(?i)\bcurl\b.+\|\s*(sh|bash|powershell|pwsh)\b",
        r"(?i)\bwget\b.+\|\s*(sh|bash|powershell|pwsh)\b",
        r"(?i)\bpowershell\b.+\b(encodedcommand|-enc)\b",
        r":\(\)\s*\{\s*:\|:\s*&\s*\}\s*;",
    )

    SECRET_PATTERNS = (
        r"(?i)\b(api[_-]?key|secret[_-]?key|access[_-]?token|auth[_-]?token|private[_-]?key|client[_-]?secret)\b\s*[:=]\s*['\"]?[A-Za-z0-9_\-./+=]{16,}",
        r"\bsk-[A-Za-z0-9]{20,}\b",
        r"\bghp_[A-Za-z0-9]{30,}\b",
        r"\bgithub_pat_[A-Za-z0-9_]{40,}\b",
        r"\bAKIA[0-9A-Z]{16}\b",
        r"-----BEGIN\s+(RSA|DSA|EC|OPENSSH|PGP)?\s*PRIVATE\s+KEY-----",
        r"(?i)\bpassword\b\s*[:=]\s*['\"]?[^'\"\s]{8,}",
    )

    BINARY_CONTENT_PATTERNS = (
        r"\x00",
        r"[\x01-\x08\x0b\x0c\x0e-\x1f]",
    )

    def validate(self, text: str) -> ValidationResult:
        """Run validation checks in order and return the first failure."""
        validators: tuple[Callable[[str], Optional[ValidationResult]], ...] = (
            self._validate_length,
            self._validate_binary_content,
            self._validate_repeated_characters,
            self._validate_prompt_injection,
            self._validate_jailbreak,
            self._validate_dangerous_requests,
            self._validate_sql_injection,
            self._validate_xss,
            self._validate_shell_commands,
            self._validate_secret_leakage,
        )

        for validator in validators:
            result = validator(text)
            if result is not None:
                return result

        return ValidationResult(True, "Input passed guardrails validation.")

    def _validate_length(self, text: str) -> Optional[ValidationResult]:
        # Empty, tiny, or extremely large prompts are rejected before model calls.
        if text is None or not text.strip():
            return ValidationResult(False, "Please describe the software you want to build.")

        length = len(text.strip())
        if length < self.MIN_LENGTH:
            return ValidationResult(
                False,
                f"Project idea is too short. Please enter at least {self.MIN_LENGTH} characters.",
            )

        if length > self.MAX_LENGTH:
            return ValidationResult(
                False,
                f"Project idea is too long. Please keep it under {self.MAX_LENGTH} characters.",
            )

        return None

    def _validate_binary_content(self, text: str) -> Optional[ValidationResult]:
        # AgentForge accepts text ideas only; binary/control payloads are rejected.
        if self._matches_any(text, self.BINARY_CONTENT_PATTERNS):
            return ValidationResult(False, "Unsupported binary or control characters detected.")

        non_printable_count = sum(
            1 for char in text if not char.isprintable() and char not in "\r\n\t"
        )
        if text and non_printable_count / len(text) > self.MAX_NON_PRINTABLE_RATIO:
            return ValidationResult(False, "Input contains too much unsupported binary content.")

        return None

    def _validate_repeated_characters(self, text: str) -> Optional[ValidationResult]:
        # Repeated character floods are commonly accidental input or low-quality abuse.
        pattern = rf"(.)\1{{{self.MAX_REPEATED_CHARACTER_COUNT},}}"
        if re.search(pattern, text, re.DOTALL):
            return ValidationResult(False, "Input contains excessive repeated characters.")

        return None

    def _validate_prompt_injection(self, text: str) -> Optional[ValidationResult]:
        # Blocks direct attempts to override or reveal hidden agent instructions.
        if self._matches_any(text, self.PROMPT_INJECTION_PATTERNS):
            return ValidationResult(False, "Prompt injection attempt detected.")

        return None

    def _validate_jailbreak(self, text: str) -> Optional[ValidationResult]:
        # Blocks common jailbreak framing before it reaches the Manager Agent.
        if self._matches_any(text, self.JAILBREAK_PATTERNS):
            return ValidationResult(False, "Jailbreak attempt detected.")

        return None

    def _validate_dangerous_requests(self, text: str) -> Optional[ValidationResult]:
        # Rejects requests to generate malware, credential theft, or abuse tooling.
        if self._matches_any(text, self.DANGEROUS_REQUEST_PATTERNS):
            return ValidationResult(False, "Dangerous software request detected.")

        return None

    def _validate_sql_injection(self, text: str) -> Optional[ValidationResult]:
        # Detects SQL injection payloads and destructive SQL fragments.
        if self._matches_any(text, self.SQL_INJECTION_PATTERNS):
            return ValidationResult(False, "SQL injection pattern detected.")

        return None

    def _validate_xss(self, text: str) -> Optional[ValidationResult]:
        # Detects common XSS payloads, event handlers, and JavaScript URL schemes.
        if self._matches_any(text, self.XSS_PATTERNS):
            return ValidationResult(False, "XSS pattern detected.")

        return None

    def _validate_shell_commands(self, text: str) -> Optional[ValidationResult]:
        # Blocks destructive shell commands and pipe-to-shell execution patterns.
        if self._matches_any(text, self.DANGEROUS_SHELL_PATTERNS):
            return ValidationResult(False, "Dangerous shell command detected.")

        return None

    def _validate_secret_leakage(self, text: str) -> Optional[ValidationResult]:
        # Prevents accidental API keys, access tokens, passwords, or private keys.
        if self._matches_any(text, self.SECRET_PATTERNS):
            return ValidationResult(False, "Potential secret or API key detected. Remove secrets before submitting.")

        return None

    @staticmethod
    def _matches_any(text: str, patterns: tuple[str, ...]) -> bool:
        return any(re.search(pattern, text, re.IGNORECASE | re.MULTILINE) for pattern in patterns)
