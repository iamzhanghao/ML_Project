def clean(word):
    word = word.replace("\n",'')
    return word.lower()


print(clean("MyNA!\n"))

print(clean("http://t.co/N7EZpu95"))

