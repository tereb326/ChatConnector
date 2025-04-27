import os

from openai import OpenAI
import urllib.request

def load_properties():
    resource_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'app.properties')
    resource_path = os.path.abspath(resource_path)

    properties = {}
    try:
        with open(resource_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key_value = line.split('=', 1)
                    if len(key_value) == 2:
                        key, value = key_value
                        properties[key.strip()] = value.strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"Plik {resource_path} nie został znaleziony.")

    return properties


def load_prop(prop, property_name):
    if property_name not in prop:
        raise KeyError(f"Brak {property_name} w pliku app.properties.")

    return prop[property_name]


class OpenAIConnector:
    def __init__(self):
        self.prop = load_properties(),
        self.client = OpenAI(
            api_key = load_prop(self.prop[0], 'api.key'),
            organization = load_prop(self.prop[0], 'api.organisation')
        )

    def invoke_text_prompt(self, prompt_text):
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {"role": "user", "content": prompt_text}
            ]
        )

        return completion.choices[0].message.content


    def create_image_with_gpt(self, prompt_text, save_to_file, file_name):
        result = self.client.images.generate(
            model="dall-e-3",
            prompt = prompt_text,
            size="1024x1024"
        )

        print(result)

        if save_to_file:
            urllib.request.urlretrieve(
                result.data[0].url,
                f"images/{file_name}")

        return result.data[0].url

    def list_my_models(self):
        models = self.client.models.list()
        for model in models.data:
            print(model.id)

