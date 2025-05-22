import random
import re
import json
from collections import defaultdict

class MarkovModel:
    def __init__(self):
        self.graph = defaultdict(list)
        
    def tokenize(self,text):
        text = re.sub(r"[^\w\s]", "", text)  #removing punctuation and numbers
        text = text.lower().strip()          #converting lower case and removing extra spaces
        return text.split()
    
    def train(self,text):
        tokens = self.tokenize(text)
        for i,token in enumerate(tokens):
            if (len(tokens)-1) == i:
                break
            self.graph[token].append(tokens[i+1])
    
    def generate(self, prompt, length=10):
        tokens = self.tokenize(prompt)
        if not tokens:
            return "Invalid prompt!"
        current = tokens[-1]
        output = prompt
        for _ in range(length):
            options = self.graph.get(current, [])
            if not options:
                break
            current = random.choice(options)
            output += f" {current}"
        return output
    
    def save_model(self, filepath):
        """Saving the trained model to a JSON file."""
        with open(filepath, 'w') as file:
            json.dump(self.graph, file)
        print(f"Model saved to {filepath}")

    def load_model(self, filepath):
        """Loading a trained model from a JSON file."""
        try:
            with open(filepath, 'r') as file:
                self.graph = json.load(file)
            print(f"Model loaded from {filepath}")
        except FileNotFoundError:
            print("File not found. Please check the file path.")
        except json.JSONDecodeError:
            print("Error loading the model. Ensure the file format is correct.")


model = MarkovModel()

# Train the model
text_data = "The sun rises in the east. The sun sets in the west."
model.train(text_data)

# Save the trained model
model.save_model("markov_model.json")

# Load the model
new_model = MarkovModel()
new_model.load_model("markov_model.json")

# Generate text using the loaded model
print(new_model.generate("The sun", length=8))
