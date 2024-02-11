# generative-ai-experiment
生成AIに関するソースコードやテキストをまとめたリポジトリ。

## Bootstrap
```shell
cp .env.sample .env

docker compose up
open http://localhost:8501 # Access to the webapp
open http://localhost:8888 # Access to the notebook
```

## Contents
### webapp
#### Simple Chat Completion
ChatGPTを使ったシンプルなチャットボット。

#### Function Calling
Function Callingを使ったシンプルな関数呼び出しと関数の結果を利用した応答を行う。

#### Recipe Generation
Function Callingの引数を利用して特定のフォーマットで応答(関数は呼ばない)。
返却された値を元にレシピを描画。
DALL-Eを使って画像を生成。

#### Text Tagging
LangChainを使ってテキストをタグ付け。LangChainから提供されている関数を呼ぶだけ。

#### PDF-based Q&A
PDFの情報を元に質問に答える。RAG。
LlamaIndexのVectorStoreIndexを使ってPDFのデータからインデックスを作成。
インデックスからエンジンを取得し、そのエンジンに質問を投げる。

#### SQL Generation
テキストを入力するとSQLの生成と実行を行い、結果を元に応答する。
LlamaIndexのNLSQLTableQueryEngineにスキーマとLLMの情報を渡す。
生成されたエンジンに質問するとSQLの生成と実行を行う。

#### Scheduling Agent
Google Calendarに予定を自動で登録するエージェント。
Google Calendarに予定を登録するwebhookを叩く関数と、現在時刻を取得する関数をtoolsとしてLangChain Agentに渡して実行。

### notebook
#### YouTube Extractor
YouTubeのURLを入力するとその動画の内容をテキストで検索できる。
pytubeを使って動画のストリームを取得し、whisperでテキストとそのテキストの再生時間を抽出。
テキストを元にFAISSでベクターストア(テキストを一定のチャンクに分割した後にEmbeddingし、Embedding後のベクトルデータをインデックスしているDB)を作成。
ベクターストアとLLMをVectorDBQAWithSourcesChainに渡して実行。

#### LangChain Agent
Serp APIをtoolsとして登録しているため、Google検索の結果を踏まえた応答ができるチャットボット。

#### OpenAI Fine Tuning
学習データを元にモデル自体の更新を行う。

#### OpenAI Image Generation
TODO

#### OpenAI Function Calling
利用可能な関数をLLMに渡して、LLMに「関数を使いたいかどうか」判断をさせる機能。
LLMが関数を実行するわけではなく、LLMは「関数を使いたいかどうか」を返してくるだけ。

#### OpenAI Chat
チャットボット。

#### Serp API
Google検索をAPI経由で行えるサービス。
