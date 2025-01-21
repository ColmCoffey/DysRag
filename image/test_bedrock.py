from langchain_aws import ChatBedrock

def test_bedrock():
    try:
        model = ChatBedrock(model_id="amazon.titan-text-lite-v1")
        response = model.invoke("Test message")
        print("Bedrock connection successful")
        print(f"Response: {response.content}")
    except Exception as e:
        print(f"Bedrock connection failed: {str(e)}")

if __name__ == "__main__":
    test_bedrock()