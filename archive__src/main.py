from textnode import text_to_textnodes, TextNode, TextType

def main():
    text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
    new_nodes = text_to_textnodes(text)
    # print(new_nodes)

if __name__ == "__main__":
    main()