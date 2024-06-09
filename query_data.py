import argparse
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from get_embedding_function import get_embedding_function
from flask import Flask, request, jsonify

from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

llm_name = "gpt-3.5-turbo"

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

app = Flask(__name__)


@app.route('/query', methods=['POST'])
def query():
    query_text = request.json['question']
    response_text = query_rag(query_text)
    return jsonify({'answer': response_text})


# def main():
#     # Create CLI.
#     parser = argparse.ArgumentParser()
#     parser.add_argument("query_text", type=str, help="The query text.")
#     args = parser.parse_args()
#     query_text = args.query_text
#     query_rag(query_text)

def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    # results = db.similarity_search_with_score(query_text, k=5)

    llm = ChatOpenAI(model_name=llm_name, temperature=0)

    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=db.as_retriever(),
        chain_type="refine",
    )

    result = qa_chain({"query": query_text})

    response_text = result["result"]

    # context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    # prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    # prompt = prompt_template.format(context=context_text, question=query_text)
    # # print(prompt)
    #
    # model = Ollama(model="mistral")
    # response_text = model.invoke(prompt)
    #
    # sources = [doc.metadata.get("id", None) for doc, _score in results]
    # formatted_response = f"Response: {response_text}\nSources: {sources}"
    # print(formatted_response)
    return response_text


if __name__ == "__main__":
    # main()
    app.run(host='0.0.0.0', port=5000, debug=True)
