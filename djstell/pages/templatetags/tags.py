from django.template import Library, Node
from django.template.defaultfilters import stringfilter
from djstell.pages.sitemap import sitemap
from djstell.pages.models import Entry, Tag, Link
from django.conf import settings

import re

register = Library()

@register.inclusion_tag('entry.html')
def blog_entry(entry, mode):
    return {'entry':entry, 'mode':mode}

@register.inclusion_tag('pmn.html')
def prev_main_next(prev, next):
    return {'prev':prev, 'next':next}

@register.inclusion_tag('sidebar.html')
def sidebar(which, force=False):
    """ Make the blogroll.
    """
    inc = settings.PHP_INCLUDE
    if force:
        inc = False
        
    c = {}
    c['which'] = which    
    c['include'] = inc
    
    if inc:
        return c

    if which == 'blog':
        c['tpt'] = False    # Not interested in showing this any more.
        c['archive_years'] = [ d.year for d in Entry.objects.dates('when', 'year', order='DESC') ]
        c['tags'] = Tag.objects.filter(sidebar=True).order_by('tag')
        c['more_tag_count'] = Tag.objects.filter(sidebar=False).count()
        c['blogroll'] = Link.objects.filter(sidebar=True).order_by('text')
        #c['tabblos'] = 'favs'
        c['rss'] = True
        c['commerce'] = True
    elif which == 'page':
        #c['tabblos'] = 'recent'
        c['youmightlike'] = True
    return c

@register.inclusion_tag('searchbox.html')
def search_box(image=True, label=''):
    return {'image':image, 'label':label}

@register.simple_tag
def year_range(year1, year2):
    """ Return a range of years, if the two years are different.
    """
    if hasattr(year1, 'year'):
        year1 = year1.year
    if hasattr(year2, 'year'):
        year2 = year2.year
    if year1 == year2:
        return str(year1)
    else:
        return "%s&ndash;%s" % (year1, year2)

special_ch = {
    '':     '',
    '>>':   '&#xbb;',
    '<<':   '&#xab;',
    '(c)':  '&#xa9;',
    'S':    '&#xa7;',
    '*':    '&#x2022;',
    '.':    '&#xb7;',
    '-':    '&#x2013;',
    '--':   '&#x2014;',
    ':>':   '&#x25b6;',
    'o':    '&#x25e6;',
    '[]':   '&#x25ab;',
    '<>':   '&#x25c7;',
    }

@register.simple_tag
def ch(value):
    return '&#xa0;'.join([special_ch[s] for s in value.split(' ')])

@register.tag
def ifnotfirst(parser, token):
    bits = token.contents.split()
    nodelist = parser.parse(('endifnotfirst',))
    parser.delete_first_token()
    return IfNotFirstNode(nodelist, *bits[1:])

class IfNotFirstNode(Node):
    def __init__(self, nodelist, *varlist):
        self.nodelist = nodelist
        self._checked = False

    def render(self, context):
        if 'forloop' in context and '_iffirst' not in context['forloop']:
            self._checked = False
            context['forloop']['_iffirst'] = True
            
        if self._checked:
            content = self.nodelist.render(context)
        else:
            content = ''
            
        self._checked = True
        return content

@register.simple_tag
def link_list(links, sep):
    links = [ "<a href='%s'>%s</a>" % (href, title) for (title, href) in links ]
    return sep.join(links)

@register.simple_tag
def top_areas():
    crumbs = sitemap.top_areas()
    links = [ "<a href='%s'>%s</a>" % (href, title) for (title, href) in crumbs ]
    return " | ".join(links)

@register.filter()
@stringfilter
def addphpslashes(value):
    """ Adds slashes for a PHP single-quoted string, in other words, only for single-quotes.
    """
    value = value.replace("'", "\\'")
    return value
addphpslashes.is_safe = True

@register.filter()
@stringfilter
def first_par(value):
    """ Take just the first paragraph of the HTML passed in.
    """
    return value.split("</p>")[0] + "</p>"

@register.filter()
@stringfilter
def first_sentence(value, number=1):
    """ Take just the first `number` sentences of the HTML passed in.
    """
    number = int(number)
    assert number > 0
    value = inner_html(first_par(value))
    words = value.split()
    # Collect words until the result is a sentence.
    sentence = ""
    while words and number > 0:
        if sentence:
            sentence += " "
        sentence += words.pop(0)
        if not re.search(r'[.?!][)"]*$', sentence):
            # A sentence has to end with punctuation.
            continue
        if words and not re.search(r'^[("]*[A-Z0-9]', words[0]):
            # Next sentence has to start with upper case.
            continue
        if re.search(r'(Mr\.|Mrs\.|Ms\.|Dr\.| [A-Z]\.)$', sentence):
            # If the "sentence" ends with a title or initial, then it probably
            # isn't the end of the sentence.
            continue
        if sentence.count('(') != sentence.count(')'):
            # A sentence has to have balanced parens.
            continue
        if sentence.count('"') % 2:
            # A sentence has to have an even number of quotes.
            continue
        
        # We have a complete sentence.
        number -= 1
    
    return sentence

@register.filter()
@stringfilter
def inner_html(value):
    """ Strip off the outer tag of the HTML passed in.
    """
    if value.startswith('<'):
        value = value.split('>', 1)[1].rsplit('<', 1)[0]
    return value

@register.filter()
@stringfilter
def widont(value):
    """ Join the last two words with an &nbsp; to prevent widowed words.
    """
    word = ''
    while value:
        value, end = value.rsplit(" ", 1)
        if word:
            word = end + ' ' + word
        else:
            word = end
        if word.count('<') == word.count('>'):
            break
    if value:
        return value + "&#xa0;" + word
    else:
        return word

@register.filter()
@stringfilter
def just_text(value):
    """ Remove non-text HTML tags (really just img for now).
    """
    # Remove all img tags
    noimg = re.sub("<img [^>]*>(</img>)?", "", value)
    # Now we might have empty <a> tags. Remove them..
    noemptya = re.sub("<a [^>]*></a>", "", noimg)
    return noemptya

from django.template.defaulttags import SpacelessNode as ReallySpacelessNode

@register.tag
def reallyspaceless(parser, token):
    nodelist = parser.parse(('endreallyspaceless',))
    parser.delete_first_token()
    return ReallySpacelessNode(nodelist)

# Our own spaceless that works the way I want.
@register.tag
def spaceless(parser, token):
    nodelist = parser.parse(('endspaceless',))
    parser.delete_first_token()
    return SpacelessNode(nodelist)

class SpacelessNode(Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        s = self.nodelist.render(context).strip()
        inline_tags = 'a|b|i|u|em|strong|sup|sub|tt|font|small|big|input|span'
        inlines_with_spaces = r'</(%s)>\s+<(%s)\b' % (inline_tags, inline_tags)
        s = re.sub(inlines_with_spaces, r'</\1>&#preservespace;<\2', s)
        s = re.sub(r'<(\w+)([^>]+)>\s+</\1>', r'<\1\2>&#preservespace;</\1>', s)
        s = re.sub(r'>\s+<', '><', s)
        s = s.replace('&#preservespace;', ' ')
        return s

if __name__ == '__main__':
    print "Sentences"
    print first_sentence("<p>A dog. A cat.")
    print first_sentence("<p>A co-worker (hi Matt!) is having a baby. A cat.</p>")
    print first_sentence('<p>A dog (canine!) said, "woof!" before. A cat.</p>')
    print first_sentence("<p>A dog <i>barked</i> loudly.</p>")
    print first_sentence('<p>A dog (canine!) said, "Woof! Woof!" before. A cat.</p>')
    print first_sentence("<p>Hello, Mr. Batchelder.</p>")
    print first_sentence("<p>A dog <i>barked</i> loudly.</p>")

    print "Text"
    print just_text("<p><a href='foo'><img src='bar'></a>My son Max</p>")