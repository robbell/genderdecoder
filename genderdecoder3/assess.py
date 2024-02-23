import re
from . import wordlists

def _make_coded_words_regex(coded_words):
    regex_group = '|'.join(coded_words)
    return re.compile(f'\\b(({regex_group})\\w*)\\b', re.IGNORECASE)

_NONASCII_RE = re.compile(r'[^\x00-\x7f]')
_FEMININE_RE = _make_coded_words_regex(wordlists.feminine_coded_words)
_MASCULINE_RE = _make_coded_words_regex(wordlists.masculine_coded_words)

def assess(ad_text):
    ad_text = _NONASCII_RE.sub(' ', ad_text)
    feminine_coded_words = [word[0] for word in _FEMININE_RE.findall(ad_text)]
    masculine_coded_words = [word[0] for word in _MASCULINE_RE.findall(ad_text)]
    
    if feminine_coded_words and not masculine_coded_words:
        result = "strongly feminine-coded"
    elif masculine_coded_words and not feminine_coded_words:
        result = "strongly masculine-coded"
    elif not masculine_coded_words and not feminine_coded_words:
        result = "neutral"
    else: 
        if len(feminine_coded_words) == len(masculine_coded_words):
            result = "neutral"
        if ((len(feminine_coded_words) / len(masculine_coded_words)) >= 2 and 
            len(feminine_coded_words) > 5):
            result = "strongly feminine-coded"
        if ((len(masculine_coded_words) / len(feminine_coded_words)) >= 2 and 
            len(masculine_coded_words) > 5):
            result = "strongly masculine-coded"
        if len(feminine_coded_words) > len(masculine_coded_words):
            result = "feminine-coded"
        if len(masculine_coded_words) > len(feminine_coded_words):
            result = "masculine-coded"
    
    if "feminine" in result:
        explanation = ("This job ad uses more words that are stereotypically feminine "
            "than words that are stereotypically masculine. Fortunately, the research "
            "suggests this will have only a slight effect on how appealing the job is "
            "to men, and will encourage women applicants.")
    elif "masculine" in result:
        explanation = ("This job ad uses more words that are stereotypically masculine "
            "than words that are stereotypically feminine. It risks putting women off "
            "applying, but will probably encourage men to apply.")
    elif not masculine_coded_words and not feminine_coded_words:
        explanation = ("This job ad doesn't use any words that are stereotypically "
            "masculine and stereotypically feminine. It probably won't be off-putting "
            "to men or women applicants.")
    else:
        explanation = ("This job ad uses an equal number of words that are "
            "stereotypically masculine and stereotypically feminine. It probably won't "
            "be off-putting to men or women applicants.")

    return {"result": result,
            "explanation": explanation,
            "masculine_coded_words": masculine_coded_words,
            "feminine_coded_words": feminine_coded_words
            }
