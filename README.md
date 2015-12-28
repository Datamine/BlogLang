# BlogLang
Small markup language for writing articles for my website at www.johnloeber.com

Existential reason: writing blog posts in pure HTML is annoying. I have to do a lot of formatting with tags, linking footnotes, etc. I'm writing a small compiler to take textfiles and turn them into HTML for my website.
I know that markdown exists, but I want the language to play nicely with my particular desires and CSS. Thus, this is markdown-inspired.

Below are the formatting options:
```
# Header  
## Subheader  
% Comment  
`Code`  
*italics*  
**bold**  
* Unordered List  
1. Ordered List   
[Linktext](URL)   
[Integer creates a footnote and a link to it]  
```

Paragraphs/breaks are indicated by double breaks between text, e.g.
> Lorem Ipsum
>
> dolor sit amet.

Some other substitutions:
* The compiler turns primes (') and double prime(") into apostrophes/single quotes (&lsquo;,&rsquo;), and double quotes (&ldquo;,&rdquo;)
* Similar for ampersands (&amp;), em-dashes (&mdash;)

If I need anything more particular, I'll edit the HTML itself. I'm thinking about adding support for images and some javascript for spoilers, but those scenarios seem sufficiently rare for me to shelve that for the moment.
