from mem0 import Memory, MemoryAgent
import os
config ={
  "version":"v1.1",
  "embedder":{
    "provider":"openai",
    "config":{
      "api_key":"YOUR_OPENAI_API_KEY","model":"text-embedding-3-large"
    }
  },
  "llm":{
    "provider":"openai",
    "config":{
      "api_key":"YOUR_OPENAI_API_KEY","model":"gpt-4o"
}},
   "graph_store":{
    "provider":"neo4j",
    "config":{
      "uri":os.environ.get("NEO_CONNECTION_URI"),
      "username":"99973a57",
      "password":" kYBg6efXynxahb1pGYKxh7X-Bvl2V_yHd_cpvGaYYdU"
    }},
  "vector_store":{
    "provider":"qdrant",
    "config":{
      "host":"localhost",
      "port":6333,
      "collection_name":"Memory"
    }
  }
}

mem_client =Memory.from_config(config)