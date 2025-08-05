from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ftfy
import re
import nltk
import spacy
import textstat
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("gemini_api_key")
genai.configure(api_key=gemini_api_key)

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

nlp = spacy.load("en_core_web_sm")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str

UNIVERSAL_REPLACEMENTS = {
    "subsequently": "later",
    "nevertheless": "however", 
    "furthermore": "also",
    "demonstrate": "show",
    "facilitate": "help",
    "utilize": "use",
    "implement": "put into practice",
    "establish": "set up",
    "maintain": "keep",
    "ensure": "make sure",
    "require": "need",
    "provide": "give",
    "determine": "find out",
    "indicate": "show",
    "consider": "think about",
    "obtain": "get",
    "receive": "get",
    "purchase": "buy",
    "commence": "start",
    "complete": "finish",
    "continue": "keep going",
    "include": "have",
    "exclude": "leave out",
    "increase": "make bigger",
    "decrease": "make smaller",
    "improve": "make better",
    "reduce": "make less",
    "eliminate": "remove",
    "prevent": "stop",
    "achieve": "reach",
    "assist": "help",
    "contribute": "add to",
    "participate": "take part",
    "collaborate": "work together",
    "communicate": "talk",
    "recommend": "suggest",
    "advise": "tell",
    "inform": "let know",
    "notify": "tell",
    "request": "ask for",
    "submit": "send in",
    "approve": "say yes to",
    "reject": "say no to",
    "accept": "take",
    "acknowledge": "recognize",
    "confirm": "make sure",
    "verify": "check",
    "examine": "look at",
    "evaluate": "judge",
    "assess": "check",
    "analyze": "study",
    "investigate": "look into",
    "research": "study",
    "monitor": "watch",
    "supervise": "oversee",
    "manage": "run",
    "operate": "run",
    "function": "work",
    "perform": "do",
    "execute": "carry out",
    "conduct": "do",
    "organize": "arrange",
    "coordinate": "work together",
    "schedule": "plan time",
    "allocate": "give out",
    "distribute": "share out",
    "deliver": "bring",
    "transport": "move",
    "transfer": "move",
    "relocate": "move",
    "install": "put in",
    "construct": "build",
    "manufacture": "make",
    "produce": "make",
    "generate": "create",
    "develop": "make",
    "design": "plan",
    "modify": "change",
    "adjust": "change",
    "adapt": "change to fit",
    "customize": "make to fit",
    "enhance": "improve",
    "upgrade": "improve",
    "update": "make current",
    "revise": "change",
    "edit": "change",
    "correct": "fix",
    "repair": "fix",
    "resolve": "solve",
    "address": "deal with",
    "handle": "deal with",
    "process": "deal with",
    "procedure": "way to do",
    "protocol": "rules",
    "policy": "rule",
    "regulation": "rule",
    "requirement": "need",
    "specification": "details",
    "criteria": "standards",
    "standard": "normal way",
    "guideline": "guide",
    "instruction": "directions",
    "documentation": "papers",
    "information": "facts",
    "data": "facts",
    "evidence": "proof",
    "reference": "source",
    "resource": "tool",
    "material": "stuff",
    "equipment": "tools",
    "instrument": "tool",
    "device": "machine",
    "system": "way of doing",
    "method": "way",
    "technique": "way",
    "approach": "way",
    "strategy": "plan",
    "solution": "answer",
    "alternative": "other choice",
    "option": "choice",
    "opportunity": "chance",
    "possibility": "chance",
    "potential": "possible",
    "capacity": "ability",
    "capability": "ability",
    "expertise": "skill",
    "knowledge": "knowing",
    "experience": "practice",
    "qualification": "training",
    "credential": "proof of training",
    "certificate": "proof",
    "license": "permission",
    "permit": "permission",
    "authorization": "permission",
    "approval": "saying yes",
    "consent": "saying yes",
    "agreement": "deal",
    "contract": "deal",
    "arrangement": "plan",
    "commitment": "promise",
    "obligation": "duty",
    "responsibility": "job",
    "accountability": "being responsible",
    "liability": "being responsible for",
    "consequence": "result",
    "outcome": "result",
    "effect": "result",
    "impact": "effect",
    "influence": "effect on",
    "benefit": "good thing",
    "advantage": "good point",
    "disadvantage": "bad point",
    "limitation": "limit",
    "restriction": "limit",
    "constraint": "limit",
    "barrier": "block",
    "obstacle": "block",
    "challenge": "hard thing",
    "difficulty": "hard thing",
    "problem": "trouble",
    "issue": "problem",
    "concern": "worry",
    "risk": "danger",
    "hazard": "danger",
    "safety": "being safe",
    "security": "being safe",
    "protection": "keeping safe",
    "prevention": "stopping",
    "emergency": "urgent problem",
    "urgent": "needs doing now",
    "immediate": "right now",
    "priority": "most important",
    "significant": "important",
    "essential": "needed",
    "necessary": "needed",
    "required": "needed",
    "mandatory": "must do",
    "optional": "choice",
    "voluntary": "choice",
    "automatic": "by itself",
    "manual": "by hand",
    "individual": "single",
    "personal": "your own",
    "private": "not public",
    "public": "for everyone",
    "general": "for most",
    "specific": "exact",
    "particular": "special",
    "unique": "one of a kind",
    "common": "normal",
    "typical": "normal",
    "standard": "normal",
    "regular": "normal",
    "frequent": "often",
    "occasional": "sometimes",
    "rare": "not often",
    "unusual": "not normal",
    "exceptional": "very special",
    "extraordinary": "amazing",
    "remarkable": "worth noting",
    "notable": "worth noting",
    "important": "matters",
    "valuable": "worth a lot",
    "useful": "helpful",
    "effective": "works well",
    "efficient": "works well with less",
    "successful": "works",
    "beneficial": "helpful",
    "positive": "good",
    "negative": "bad",
    "neutral": "neither good nor bad",
    "reasonable": "makes sense",
    "appropriate": "right for",
    "suitable": "right for",
    "adequate": "enough",
    "sufficient": "enough",
    "insufficient": "not enough",
    "excessive": "too much",
    "minimum": "least",
    "maximum": "most",
    "average": "normal amount",
    "approximately": "about",
    "exactly": "just right",
    "precisely": "exactly",
    "accurately": "correctly",
    "correctly": "right way",
    "properly": "right way",
    "effectively": "in a way that works",
    "efficiently": "without waste",
    "quickly": "fast",
    "slowly": "not fast",
    "immediately": "right now",
    "eventually": "in the end",
    "finally": "at last",
    "initially": "at first",
    "originally": "at first",
    "previously": "before",
    "currently": "now",
    "presently": "now",
    "recently": "not long ago",
    "temporarily": "for a short time",
    "permanently": "forever",
    "continuously": "without stopping",
    "frequently": "often",
    "regularly": "on schedule",
    "consistently": "always the same way",
    "constantly": "all the time"
}

def clean_text(text):
    text = ftfy.fix_text(text)
    text = ''.join(c for c in text if c.isprintable())
    text = re.sub(r'[\r\n]+', '\n', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

def segmentation_text(text):
    paragraph = [p for p in text.split('\n') if p.strip()]
    sentance = []
    for para in paragraph:
        sentance.extend(nltk.sent_tokenize(para))
    tokens = [nltk.word_tokenize(sent) for sent in sentance]
    return {
        'paragraph': paragraph,
        'sentences': sentance,
        'tokens': tokens,
    }

def readability_score(text):
    return{
        "flesch_reading_ease" : textstat.flesch_reading_ease(text),
        "flesch_kincaid_grade" : textstat.flesch_kincaid_grade(text),
        "gunning_fog": textstat.gunning_fog(text),
        "smog_index": textstat.smog_index(text),
        "coleman_liau_index" : textstat.coleman_liau_index(text),
        "automated_readability_index" : textstat.automated_readability_index(text),
        "dale_chall_readability_score" : textstat.dale_chall_readability_score(text),
        "difficult_words_count" : textstat.difficult_words(text),
        "difficult_words_list" : textstat.difficult_words_list(text),
    }

def detect_long_sentance(sentances, threshold=25):
    return [sent for sent in sentances if len(sent.split()) > threshold]

def detect_passive_voice(sentences):
    passive_sentences = []
    for sent in sentences:
        doc = nlp(sent)
        for token in doc:
            if token.dep_ == "nsubjpass":
                passive_sentences.append(sent)
                break
    return passive_sentences

def detect_ambiguous_structures(sentences):
    ambiguous_keywords = ["might", "could", "possibly", "maybe", "potentially", "approximately", "suggests", "appears"]
    return [sent for sent in sentences if any(word in sent.lower() for word in ambiguous_keywords)]

def assesment_data(preprocessed_text):
    paragraph = "".join(preprocessed_text['paragraph'])
    sentences = preprocessed_text["sentences"]
    return{
        "readability_score" : readability_score(paragraph),
        "long_sentences" : detect_long_sentance(sentences),
        "passive_voice" : detect_passive_voice(sentences),
        "detect_ambiguous_structures" : detect_ambiguous_structures(sentences),
    }

def lexical_simplify(text):
    words = nltk.word_tokenize(text)
    simplified_words = []
    
    for word in words:
        clean_word = re.sub(r'[^\w]', '', word.lower())
        
        if clean_word in UNIVERSAL_REPLACEMENTS:
            replacement = UNIVERSAL_REPLACEMENTS[clean_word]
            if word and word[0].isupper():
                replacement = replacement.capitalize()
            if word != clean_word and len(word) > len(clean_word):
                punct = word[len(clean_word):]
                replacement += punct
            simplified_words.append(replacement)
        else:
            simplified_words.append(word)
    
    return ' '.join(simplified_words)

def sentence_split(sentence, max_words=18):
    words = sentence.split()
    if len(words) <= max_words:
        return [sentence]
    
    connectors = [' and ', ' but ', ' however ', ' although ', ' while ', ' because ']
    
    for connector in connectors:
        if connector in sentence:
            parts = sentence.split(connector, 1)
            if len(parts) == 2 and len(parts[0].split()) > 8:
                first_part = parts[0].strip()
                second_part = parts[1].strip()
                
                if not first_part.endswith('.'):
                    first_part += '.'
                if not second_part[0].isupper():
                    second_part = second_part.capitalize()
                if not second_part.endswith('.'):
                    second_part += '.'
                
                return [first_part, second_part]
    
    if ',' in sentence:
        comma_pos = sentence.rfind(',', 0, len(sentence)//2 + 30)
        if comma_pos > len(sentence)//4:
            first_part = sentence[:comma_pos].strip() + '.'
            second_part = sentence[comma_pos+1:].strip()
            if not second_part[0].isupper():
                second_part = second_part.capitalize()
            if not second_part.endswith('.'):
                second_part += '.'
            return [first_part, second_part]
    
    mid = len(words) // 2
    first_part = ' '.join(words[:mid]) + '.'
    second_part = ' '.join(words[mid:])
    if not second_part[0].isupper():
        second_part = second_part.capitalize()
    if not second_part.endswith('.'):
        second_part += '.'
    
    return [first_part, second_part]

def fix_grammar_issues(sentence):
    sentence = sentence.replace("putting into practice of", "implementing")
    sentence = sentence.replace("the improvement of", "improving")
    sentence = sentence.replace("the distribution of", "distributing")
    sentence = sentence.replace("connecting different transport connections", "transport connections")
    sentence = sentence.replace("rule-based following rules", "following regulations")
    sentence = sentence.replace("giving power", "empowerment")
    
    sentence = re.sub(r'\s+,', ',', sentence)
    sentence = re.sub(r',\s*\.', '.', sentence)
    sentence = re.sub(r'\s+\.', '.', sentence)
    
    sentence = sentence.strip()
    if sentence:
        sentence = sentence[0].upper() + sentence[1:]
        if not sentence.endswith('.'):
            sentence += '.'
    
    return sentence

def merge_sentence_fragments(sentences):
    merged = []
    i = 0
    
    while i < len(sentences):
        current = sentences[i].strip()
        
        if i + 1 < len(sentences):
            next_sent = sentences[i + 1].strip()
            if next_sent.startswith(('And ', 'But ', 'Or ')):
                connector = next_sent.split()[0].lower()
                rest = ' '.join(next_sent.split()[1:])
                
                if current.endswith('.'):
                    current = current[:-1]
                merged_sentence = f"{current} {connector} {rest}"
                merged.append(merged_sentence)
                i += 2
                continue
        
        merged.append(current)
        i += 1
    
    return merged

def comprehensive_simplify(text):
    grade_level = textstat.flesch_kincaid_grade(text)
    
    if grade_level <= 12:
        max_sentence_length = 20
    elif grade_level <= 20:
        max_sentence_length = 18
    else:
        max_sentence_length = 15
    
    sentences = nltk.sent_tokenize(text)
    simplified_sentences = []
    
    for sentence in sentences:
        split_sentences = sentence_split(sentence, max_sentence_length)
        
        for split_sent in split_sentences:
            simplified = lexical_simplify(split_sent)
            simplified = fix_grammar_issues(simplified)
            simplified_sentences.append(simplified)
    
    simplified_sentences = merge_sentence_fragments(simplified_sentences)
    
    return simplified_sentences

def calculate_similarity(original, simplified_list):
    simplified_text = ' '.join(simplified_list)
    
    orig_words = set(original.lower().split())
    simp_words = set(simplified_text.lower().split())
        
    adjusted_simp = set()
    for word in simp_words:
        original_word = None
        for complex_word, simple_word in UNIVERSAL_REPLACEMENTS.items():
            if simple_word.lower() == word.lower():
                original_word = complex_word
                break
        
        if original_word and original_word in orig_words:
            adjusted_simp.add(original_word)
        else:
            adjusted_simp.add(word.lower())
    
    overlap = len(orig_words.intersection(adjusted_simp))
    total = len(orig_words.union(adjusted_simp))
    
    return overlap / total if total > 0 else 0

def gemini_process(text, full_result):
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    You are an expert at creating dyslexia-friendly text.

    Here is the original text:
    {text}

    Here is an incomplete simplified version with the readabilty score:
    {full_result}

    Instructions:
    - Use both the original and the simplified version to create a single, complete, easy-to-read paragraph suitable for someone with dyslexia.
    - Make sure the meaning of the original is preserved, but use short sentences, simple words, and clear structure.
    - Fill in any missing parts or incomplete ideas from the simplified version using the original text for context.
    - The final result should be one clear, readable paragraph in plain language, suitable for dyslexic readers.

    Return only the completed simplified paragraph.
    """

    response = model.generate_content(prompt)
    return response.text

@app.post("/simplif")
async def simplify_text(request: TextRequest):
    try:
        text = request.text
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        clean_text_result = clean_text(text)
        preprocessed_text = segmentation_text(text)
        
        original_grade = textstat.flesch_kincaid_grade(text)
        difficult_words = textstat.difficult_words(text)
        simplified_sentences = comprehensive_simplify(text)
        simplified_text = ' '.join(simplified_sentences)
        final_grade = textstat.flesch_kincaid_grade(simplified_text)
        improvement = original_grade - final_grade
        similarity = calculate_similarity(text, simplified_sentences)
        
        full_result = f"""
=== UNIVERSAL DYSLEXIALENS SIMPLIFICATION ===
Original text grade level: {original_grade:.1f}
Difficult words: {difficult_words}

=== SIMPLIFIED TEXT ===
""" + '\n'.join([f"{i+1}. {s}" for i, s in enumerate(simplified_sentences)]) + f"""

=== RESULTS ===
Original grade level: {original_grade:.1f}
Simplified grade level: {final_grade:.1f}
Improvement: {improvement:.1f} grades easier
Meaning preservation: {similarity:.2f}
"""
        
        # Get final result from Gemini
        final_simplified_text = gemini_process(text, full_result)
        
        return final_simplified_text
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "DyslexiaLens API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)