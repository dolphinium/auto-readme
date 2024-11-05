
# NLP Summarizer

> This is a basic demonstration of auto-readme working on jupyter notebook(.ipynb) files. \
This feature will be added later on. 

## Project Overview

This project includes a Jupyter notebook (`nlp_summarize_gradio.ipynb`) that demonstrates the use of various Python libraries to achieve text summarization and entity recognition tasks. The notebook contains code snippets that illustrate how to use helper functions for API requests, how to summarize text, and how to close Gradio servers that are running on different ports.

## Dependencies

To use this project, you'll need to have the following Python packages installed:

- `os`
- `io`
- `IPython`
- `requests`
- `json`
- `gradio`

## Usage

### Text Summarization

The project provides a function to summarize text using an NLP model. Here's an example of how to use the summarization function:

```python
import gradio as gr

def summarize(input):
    output = get_completion(input)
    return output

# Example usage
text = '''The tower is 324 metres (1,063 ft) tall, about the same height
          as an 81-storey building, and the tallest structure in Paris. 
          Its base is square, measuring 125 metres (410 ft) on each side.'''

summary = summarize(text)
print(summary)
```

### Named Entity Recognition (NER)

The project also includes a function to perform named entity recognition using a specified API endpoint. Here's an example of how to use the NER function:

```python
text = "My name is Andrew, I'm building DeepLearningAI and I live in California"
entities = get_completion(text, parameters=None, ENDPOINT_URL=HF_NER_API_URL)
print(entities)
```

### Running Gradio Interface

To run the Gradio interface for summarization, you can use the following code:

```python
import gradio as gr

def summarize(input):
    output = get_completion(input)
    return output

gr.Interface(fn=summarize, inputs="text", outputs="text").launch()
```

## Additional Notes

- Ensure that all required dependencies are installed before running the code.
- Close any running Gradio servers if you encounter port conflicts using `gr.close_all()`.
- The project includes placeholders for testing with Turkish BERT, which can be explored further.

For further customizations and enhancements, users are welcome to modify the provided code snippets according to their project needs.
