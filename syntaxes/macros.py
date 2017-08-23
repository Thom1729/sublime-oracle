from YAMLMacros.lib.syntax import meta, expect, pop_on, stack

def meta_set(scope):
    return [
        { 'meta_scope': scope },
        { 'clear_scopes': 1 },
        { 'match': r'', 'pop': True },
    ]

def expect_keyword(match, scope="keyword.other.sql", set_context=None):
    return expect(word(match), scope, set_context)

def expect_identifier(scope):
    return [
        { 'match': r'{{unquoted_identifier}}', 'scope': scope, 'pop': True },
        {
            'match': r'(")([^"]+)(")',
            'scope': 'string.quoted.double.sql',
            'captures': {
                '1': 'punctuation.definition.string.begin.sql',
                '2': scope,
                '3': 'punctuation.definition.string.end.sql',
            },
            'pop': True,
        },

        { 'match': r'(?=\S)', 'pop': True },
    ]
    
def expect_in_parens(contents):
    return [
        {
            'match': r'\(',
            'scope': 'punctuation.section.group.begin.sql',
            'set': [
                expect(r'\)', 'punctuation.section.group.end.sql'),
                contents,
            ],
        },
        { 'match': r'(?=\S)', 'pop': True },
    ]

def end(keyword=None):
    if bool(keyword):
        next_context = expect_keyword(keyword, 'keyword.control.sql')
    else:
        next_context = expect_identifier('variable.other.label.sql')

    return {
        'match': word('END'),
        'scope': 'keyword.control.sql',
        'set': next_context,
    }

def word(match):
    return r'(?i)\b(?:%s)\b' % match

def word_ahead(match):
    return r'(?i)\b(?=(?:%s)\b)' % match

def empty_context(*args):
    return [ { 'match':'', 'pop': True } ]

def all(*contexts):
    return [
        { 'include': context } for context in contexts
    ]

def heredoc(start, end):
    return {
        'match': r"(?i)q\'%s" % start,
        'scope': 'punctuation.definition.string.begin.sql',
        'set': [
            { 'meta_include_prototype': False },
            { 'meta_scope': 'string.quoted.heredoc.sql' },
            {
                'match': r"%s\'" % end,
                'scope': 'punctuation.definition.string.end.sql',
                'pop': True,
            },
        ],
    }