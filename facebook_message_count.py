from html.parser import HTMLParser
import sys

debug = False

class FbHTMLParser(HTMLParser):
    def __init__(self, name_of_message):
        super().__init__()
        self.enter_messages_flag = False
        self.in_message_flag = False
        self.enter_message_chunk = False
        self.message_count = 0
        self.count_tags = 0
        self.level = 0
        self.enter_messages_level = -1
        self.in_message_level = -1
        self.enter_message_chunk_level = -1
        self._messages = False
        self.name_of_message = name_of_message
        self.tag_dict = {}

    def handle_starttag(self, tag, attrs):
        if not (tag == 'img' or tag == 'input' or tag == 'br'):
            self.level += 1

        if attrs and len(attrs[0]) >= 2:
            if attrs[0][1] == self.name_of_message:
                self.enter_messages_level = self.level
                self.enter_message_chunk_level = self.enter_messages_level + 2
                self.in_message_level = self.enter_message_chunk_level + 3
                self.enter_messages_flag = True

        if self.enter_messages_flag and self.level == self.enter_message_chunk_level:
            if tag == 'div' and not attrs:
                self.enter_message_chunk = True

        if self.enter_message_chunk and self.level == self.in_message_level:
            if tag == 'h5':
                self._messages = True
            elif self._messages and tag == 'div':
                self.message_count += 1
                self.in_message_flag = True

        if not tag in self.tag_dict:
            self.tag_dict[tag] = 0

        self.tag_dict[tag] += 1


    def handle_endtag(self, tag):
        self.level -= 1
        if self.in_message_flag and self.level < self.in_message_level:
            self.in_message_flag = False
        if self.enter_message_chunk and self.level < self.enter_message_chunk_level:
            self.enter_message_chunk = False
            self._messages = False
        if self.enter_messages_flag and self.level < self.enter_messages_level:
            self.enter_messages_flag = False

        self.tag_dict[tag] -= 1

    def handle_data(self, data):
        if self.in_message_flag:
            if(debug):
                print(data)



def main(text_to_parse, name_of_message='Meddelanden'):
    parser = FbHTMLParser(name_of_message)
    parser.feed(text_to_parse)
    print("Count:", parser.message_count)
    print("Level:", parser.level)
    print("tags:", parser.tag_dict)


if __name__ == '__main__':
    if len(sys.argv) > 3:
        debug = True
    if len(sys.argv) > 2:
        name_of_message = sys.argv[2]
        main(open(sys.argv[1]).read(), name_of_message)
    elif len(sys.argv) > 1:
        #try:
        main(open(sys.argv[1]).read())
        #except:
            #print("No such file")
    else:
        print('Needs an input file with text to parse')
