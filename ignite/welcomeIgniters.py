class Cookie:
    def __init__(self, taste, size, texture, is_spicy=False, shape="circle"):
        self.taste = taste
        self.size = size
        self.texture = texture
        self.is_spicy = is_spicy
        self.shape = shape

    def get_info(self):
        match self.taste:
            case "Chocolate":
                return 1
            case "Raspberry":
                return 2
            case "Matcha":
                return 3
            case _:
                return 4


def welcomeMessage():
    return "Welcome Igniters!"


def say_hello(s):
    return "Hello " + s


def magic_number(a, b):
    return ((a * b) / (a + b)) - b


def is_even(number):
    """Returns True if the number is even, False otherwise."""
    return number % 2 == 0


def reverse_string(s):
    """Returns the reverse of the input string."""
    return s[::-1]


def plus_one(a):
    return a + 1


def uppercase_string(s):
    if not isinstance(s, str):
        raise TypeError("Input must be a string.")
    return s.upper()


class EmailSender:
    def send_email(self, recipient, subject, body):
        # Simulate sending an email (in real code, this would send)
        print(f"Sending email to {recipient} with subject '{subject}'")
        return True

    def get_inbox_count(self, user):
        # Simulate checking the inbox (in real code, this would query a server)
        print(f"Checking inbox for {user}")
        return 5

    def delete_email(self, email_id):
        # Simulate deleting an email
        print(f"Deleting email with id {email_id}")
        return True
