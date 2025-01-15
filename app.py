from flask import Flask, render_template, request, jsonify, session
import openai

app = Flask(__name__)
app.secret_key = 'supersecretkey'
# Set your OpenAI API key here you can also set in .env
openai.api_key = 'sk-xxxxxxxxxxxx'

def llm(history):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a Helpful assistant."},
                {"role": "user", "content": f"""
                    You have to do this and this.
                    Instructions:
                    1.
                    2.
                    3.
                 
                    chat_history:{history}"""}
            ]
        )
        bot_response = response.choices[0].message.content
        
        return bot_response
    except openai.error.OpenAIError as e:
        return f"An error occurred: {str(e)}"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start',methods=["POST","GET"])
def bot():
    session.clear()
    return render_template('bot.html')

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form['msg']
    history = session.get('history', '')
    history += f"user: {user_input}\n"
    answer = llm(history)
    history += f"bot: {answer}\n"
    session['history'] = history
        
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')