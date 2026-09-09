from ollama import chat

messages = []

print("🤖 Chatbot started! Type 'exit' to stop.\n")

while True:

    user_query = input("You: ")

    if user_query.lower() == "exit":
        print("Bot: Goodbye! 👋")
        break

    messages.append({
        'role': 'user',
        'content': user_query
    })

    response = chat(
        model='llama3.2:latest',
        messages=messages
    )

    bot_response = response.message.content

    print("Bot:", bot_response)

    messages.append({
        'role': 'assistant',
        'content': bot_response
    })