import os
import google.generativeai as genai


def execute(query):
    genai.configure(api_key="AIzaSyDFLusJx_z5JA0tiZhCK6BjILpMD1-7YcY")
    model = genai.GenerativeModel('gemini-pro')  # 'gemini-pro' specifies the model version

    try:
        response = model.generate_content("Answer with respect to MAHABHARAT only."+query)
        return(response.text)
    except Exception as e:
        return(f"An error occurred: {e}")
    


# # Create the model
# generation_config = {
#   "temperature": 1,
#   "top_p": 0.95,
#   "top_k": 40,
#   "max_output_tokens": 8192,
#   "response_mime_type": "text/plain",
# }

# model = genai.GenerativeModel(
#   model_name="gemini-1.5-flash",
#   generation_config=generation_config,
# )

# chat_session = model.start_chat(
#   history=[]
# )

# response = chat_session.send_message("who was the lady who used to stay blindfolded in mahabharat?")

# print(response.text)