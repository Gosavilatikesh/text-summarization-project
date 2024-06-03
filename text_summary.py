import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

text = """Lorem, ipsum dolor sit amet consectetur adipisicing elit. Ex adipisci consequatur officiis maiores recusandae perspiciatis facilis exercitationem repellat tenetur Fugiat doloribus asperiores vero. Asperiores accusantium atque labore totam voluptatem. Numquam quibusdam dicta possimus placeat Lorem ipsum dolor sit amet consectetur adipisicing elit. Rerum cupiditate, modi officiis, eveniet ea voluptatum eos pariatur deserunt cum ipsum exercitationem, odio laboriosam tenetur. Reprehenderit fugit nostrum id voluptatibus modi Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam nemo in totam vero accusantium magnam ea distinctio aut dicta eaque libero velit nulla, aliquam dolorem similique laborum, voluptate id Enim. Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime sunt quisquam sequi. In, veniam non. Molestias ut modi iure quasi, doloribus, laboriosam nam facilis corrupti velit eaque, hic tenetur eos. Lorem ipsum, dolor sit amet consectetur adipisicing elit. Pariatur optio, animi laborum commodi quos facilis est blanditiis non distinctio ullam eveniet labore quam voluptas illum impedit sequi quod quisquam ea? """


def summarizer(rawdocs):
    stopwords = list(STOP_WORDS)
    # print(stopwords)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawdocs)
    #print(doc)
    token = [token.text for token in doc]
    #print(token)
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
           if word.text not in word_freq.keys():
              word_freq[word.text] = 1
           else:
              word_freq[word.text] += 1
               
    #print(word_freq)            

    max_freq = max(word_freq.values())
    #print(max_freq)

    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq
     
    #print(word_freq)     

    sent_tokens = [sent for sent in doc.sents]
    #print(sent_tokens)

    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
               if sent not in sent_scores.keys():
                  sent_scores[sent] = word_freq[word.text]
               else:
                  sent_scores[sent] += word_freq[word.text]
                
    #print(sent_scores)    

    select_len = int(len(sent_tokens) * 0.3)
    #print(select_len) 

    summary = nlargest(select_len, sent_scores, key = sent_scores.get)     
    #print(summary)

    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    #print(text)
    #print(summary)
    #print("Length of original text",len(text.split(' ')))
    #print("Length of original text",len(summary.split(' ')))
     
    return summary,  doc, len(rawdocs.split(' ')), len(summary.split(' '))                    
        