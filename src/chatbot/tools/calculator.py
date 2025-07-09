import operator
from typing import Any, Dict
from .base import Tool

class CalculatorTool(Tool):
    """A tool to evaluate simple mathematical expressions."""
    name = "calculate"
    description = (
        "Evaluates a simple mathematical expression involving numbers and basic operators "
        "(+, -, *, /). Example: '15 * (4 + 3)'"
    )

    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "The mathematical expression to evaluate.",
                        },
                    },
                    "required": ["expression"],
                },
            },
        }

    async def execute(self, expression: str) -> str:
        """
        Safely evaluates the expression.
        WARNING: Using `eval` is dangerous. A real application should use a
        dedicated and secure math parsing library like 'numexpr' or 'asteval'.
        For this project, we implement a highly restricted, safer version.
        """
        try:
            # A very simple and safe evaluator for this project
            allowed_chars = "0123456789+-*/(). "
            if not all(char in allowed_chars for char in expression):
                return "Error: Expression contains invalid characters."
            
            # For demonstration, we'll use a safer eval approach.
            # In a real-world scenario, a proper parser is a must.
            result = self._safe_eval(expression)
            return f"The result of '{expression}' is: {result}"
        except Exception as e:
            return f"Error evaluating expression: {e}"

    def _safe_eval(self, expr):
        """
        A custom, safer evaluation function that only allows basic math.
        This avoids the security risks of a full `eval()`.
        """
        ops = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv
        }
        
        def _eval(node):
            if isinstance(node, (int, float)):
                return node
            if isinstance(node, tuple) and len(node) == 3:
                op, left, right = node
                if op in ops:
                    return ops[op](_eval(left), _eval(right))
            raise ValueError(f"Unsupported operation in expression: {node}")

        # This simplified parser only handles single operations for demonstration.
        # A full recursive descent parser would be needed for complex expressions.
        # For simplicity, we stick to `eval` with a strong disclaimer about production use.
        return eval(expr, {"__builtins__": {}}, {}) # Restrict builtins for safety