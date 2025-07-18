from cleaning import clean_text

text = "@user This is an #awful comment!! 😡😠 http://hate.com"
cleaned = clean_text(text)
print("Before:", text)
print("After:", cleaned)
