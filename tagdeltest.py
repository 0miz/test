import os
from collections import Counter
import re
import gradio as gr

def load_tags(file_path):
    with open(file_path, 'r') as f:
        return [tag.strip() for tag in f.read().split(',')]

def save_tags(file_path, tags):
    with open(file_path, 'w') as f:
        f.write(', '.join(tags))

def tag_modifier(folder_path, indices_to_delete):
    folder_path = folder_path.strip('"')
    tag_counter = Counter()

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            tags = load_tags(os.path.join(folder_path, file_name))
            tag_counter.update(tags)

    tags_and_counts = [(tag, count) for tag, count in tag_counter.most_common()]

    indices_to_delete = indices_to_delete.strip()
    if indices_to_delete:
        indices_to_delete = list(map(int, re.split(r'\s*,\s*', indices_to_delete)))

        tags_to_delete = {tag for i, (tag, count) in enumerate(tag_counter.most_common(), start=1) if i in indices_to_delete}

        for file_name in os.listdir(folder_path):
            if file_name.endswith('.txt'):
                file_path = os.path.join(folder_path, file_name)
                tags = load_tags(file_path)
                tags = [tag for tag in tags if tag not in tags_to_delete]
                save_tags(file_path, tags)
    else:
        tags_to_delete = []

    tags_and_counts_string = "\n".join([f"{i+1}. {tag} ({count} times)" for i, (tag, count) in enumerate(tags_and_counts)])
    deleted_tags_string = f"Deleted tags: {', '.join(tags_to_delete)}"

    return tags_and_counts_string, deleted_tags_string

iface = gr.Interface(fn=tag_modifier, 
                     inputs=["text", "text"], 
                     outputs=["text", "text"],
                     description="Enter the folder path and the indices of tags to delete, separated by commas.")
iface.launch()
