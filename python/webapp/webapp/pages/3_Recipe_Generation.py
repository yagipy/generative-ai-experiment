import streamlit as st
import json
import openai
from pydantic import BaseModel, Field

class Ingredient(BaseModel):
    ingredient: str = Field(description="材料", examples=["鶏もも肉"])
    quantity: str = Field(description="分量", examples=["300g"])

class Recipe(BaseModel):
    ingredients: list[Ingredient]
    instructions: list[str] = Field(description="手順", examples=["材料を切ります。", "材料を炒めます。"])
    in_english: str = Field(description="料理名の英語")


OUTPUT_RECIPE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "output_recipe",
            "description": "レシピを出力する",
            # jsonをそのまま書いても動作する
            "parameters": Recipe.schema(),
        },
    }
]

SAMPLE_JSON = """
{
  "ingredients": [
    {
      "name": "材料A",
      "quantity": "1個"
    },
    {
      "name": "材料B",
      "quantity": "100g"
    }
  ],
  "instructions": [
    "材料を切ります。",
    "材料を炒めます。"
  ]
}
"""

PROMPT_TEMPLATE = """料理のレシピを考えてください。

料理名: {dish}
"""

st.title('Recipe Generation')

dish = st.text_input(label="料理名")

if dish:
    with st.spinner(text="生成中..."):
        messages = [
            {
                "role": "user",
                "content": PROMPT_TEMPLATE.format(dish=dish),
            }
        ]
        # TODO: Json Modeを使用する形にリファクタ
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            tools=OUTPUT_RECIPE_TOOLS,
            tool_choice={"type": "function", "function": {"name": OUTPUT_RECIPE_TOOLS[0]["function"]["name"]}},
        )

        response_message = response.choices[0].message
        function_call_args = response_message.tool_calls[0].function.arguments
        recipe = json.loads(function_call_args)

        st.write("## 材料")
        st.table(recipe["ingredients"])

        instruction_markdown = "## 手順\n"
        for i, instruction in enumerate(recipe["instructions"]):
            instruction_markdown += f"{i+1}. {instruction}\n"
        st.write(instruction_markdown)

        response = openai.images.generate(
            model="dall-e-3",
            prompt=recipe["in_english"],
            size="1024x1024",
            quality="standard",
            n=1,
        )
        st.image(response.data[0].url, caption="料理の画像", use_column_width=True)
