from langchain.llms import HuggingFaceHub,CTransformers
from langchain_community.chat_models import ChatYandexGPT,GigaChat


def init_mistral_cpu_instruct(huggingface_access_token) -> Any:
    llm = CTransformers(
        model="TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
        model_file = "mistral-7b-instruct-v0.2.Q4_K_M.gguf",
        model_type = "mistral",
        token=huggingface_access_token,
        source="HuggingFace",
    )
    return llm
    
def init_mistral_gpu_instruct() -> Any:
    pass


