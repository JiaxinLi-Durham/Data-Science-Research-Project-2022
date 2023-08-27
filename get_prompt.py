import pandas as pd
import time
import openai

txt_file_path = 'input you txt file path'
output_csv_path = 'output your csv file path'

def split_text(filename):
    with open(txt_file_path, 'r') as f:
        txt = f.read()

    paragraphs = txt.split('\n')

    result = []
    current_segment = ''
    word_count = 0

    for paragraph in paragraphs:
        current_segment += paragraph + "\n\n"
        word_count += len(paragraph.split())
        # word_count += len(paragraph)

        if word_count >= 400:
            result.append(current_segment)
            current_segment = ""
            word_count = 0

        # if len(result) >= 10:
        #     break

    if current_segment:
        result.append(current_segment)

    return result

segments = split_text(txt_file_path)

total_part = len(segments)
print("Data reading complete, {} sections in total.".format(total_part))




FLAG = 0
def translate_text(text):
    global FLAG
    # so that the program can run faster
    if FLAG % 2 == 1:
        openai.api_key = "Your openai api key"
    else:
        openai.api_key = "Your openai api key"


    prompt='Here is the text content that needs to be illustrated: \n"{}"'.format(text)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are an assistant illustrator who needs to extract the most suitable illustration concepts based on the article content and convey them to the illustrator using English keywords. Here is a possible example of keyword output, and you should follow this format: \nkeywords:  1boy, holding steel fork, wild boar, sandy beach, golden moon, green watermelons, escape, deep blue sky.\nYou don't need to provide any additional information."},
                {"role": "user", "content": prompt},
            ]
        )
    translation = response['choices'][0]['message']['content'].strip()

    return translation


total_result_both_language = pd.DataFrame(columns=['original_txt', 'translated_txt'])
chapter_count = 0



for segment in segments:
    # print(segment)
    chapter_count += 1
    FLAG += 1
    start_time = time.time()
    print("Translating part {}, out of {} parts.".format(chapter_count, total_part))

    english_text = segment
    translation = translate_text(english_text)
    if translation[:10] == 'keywords: ': # do not delete the space
        translation = translation[10:]
    translation = translation + ', masterpiece, best quality, illustration.'

    total_result_both_language = pd.concat([total_result_both_language, pd.DataFrame({'original_txt': [english_text], 'translated_txt': [translation]})])
        # both_language = "story \n\n Part {}: \n\n -------------------------------- \n\n".format(
        #     int(chapter_count / split_num +1)
        # )

    end_time = time.time()
    spend_time = end_time - start_time
    print("Translation time: {} seconds.".format(spend_time))
    if spend_time <20:
        print("rest {} seconds.".format(20 - spend_time))
        time.sleep(22 - spend_time)
    print("--------------------------------")
    # time.sleep(1)

total_result_both_language.to_csv(output_csv_path, index=False, encoding='utf-8')

