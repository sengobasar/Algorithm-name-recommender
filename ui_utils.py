"""
UI Utilities for professional console output
"""
from enum import Enum

class MessageType(Enum):
    HEADER = 1
    SUCCESS = 2
    INFO = 3
    WARNING = 4
    ERROR = 5
    STEP = 6
    RESULT = 7

class ConsoleUI:
    """Handles consistent console output formatting"""
    
    # ANSI color codes
    COLORS = {
        'HEADER': '\033[95m',
        'BLUE': '\033[94m',
        'CYAN': '\033[96m',
        'GREEN': '\033[92m',
        'YELLOW': '\033[93m',
        'RED': '\033[91m',
        'BOLD': '\033[1m',
        'UNDERLINE': '\033[4m',
        'END': '\033[0m'
    }
    
    @classmethod
    def format_message(cls, message: str, msg_type: MessageType) -> str:
        """Format a message with appropriate styling"""
        if msg_type == MessageType.HEADER:
            return f"\n{cls.COLORS['BLUE']}{'='*80}\n{message}\n{'='*80}{cls.COLORS['END']}\n"
        elif msg_type == MessageType.SUCCESS:
            return f"{cls.COLORS['GREEN']}[✓] {message}{cls.COLORS['END']}"
        elif msg_type == MessageType.INFO:
            return f"{cls.COLORS['CYAN']}[i] {message}{cls.COLORS['END']}"
        elif msg_type == MessageType.WARNING:
            return f"{cls.COLORS['YELLOW']}[!] {message}{cls.COLORS['END']}"
        elif msg_type == MessageType.ERROR:
            return f"{cls.COLORS['RED']}[✗] {message}{cls.COLORS['END']}"
        elif msg_type == MessageType.STEP:
            return f"\n{cls.COLORS['BLUE']}{'='*60}\n{message.upper()}\n{'='*60}{cls.COLORS['END']}"
        elif msg_type == MessageType.RESULT:
            return f"{cls.COLORS['CYAN']}  • {message}{cls.COLORS['END']}"
        return message
    
    @classmethod
    def print_message(cls, message: str, msg_type: MessageType):
        """Print a formatted message to the console"""
        print(cls.format_message(message, msg_type))
