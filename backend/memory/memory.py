class ConversationMemory:

    def __init__(self):

        self.messages = []

    def add_message(
        self,
        role,
        content
    ):

        self.messages.append(
            {
                "role": role,
                "content": content
            }
        )

    def get_history(
        self,
        limit=10
    ):

        return self.messages[-limit:]

    def get_last_user_message(
        self
    ):

        user_messages = [

            msg["content"]

            for msg in self.messages

            if msg["role"] == "user"
        ]

        if len(user_messages) < 2:

            return None

        return user_messages[-2]