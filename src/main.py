from textnode import TextNode, TextType

def main():
    test_node = TextNode("Here's an anchor", TextType.LINK, "https://www.google.com")
    print(test_node)

if __name__ == "__main__":
    main()