from YAMLMacros.lib.syntax import meta, stack, rule

def expect(expr, scope, set_context=None):
    ret = [
        rule(match=expr, scope=scope),
        # { "match": r'(?=\S)', "pop": True },
        pop_unless(expr)
    ]

    if set_context:
        ret[0]['set'] = set_context
    else:
        ret[0]['pop'] = True

    return ret

def pop_on(expr):
    return rule(
        match=r'(?=\s*(?:%s))' % expr,
        pop=True
    )

def pop_unless(expr):
    return rule(
        match=r'(?=\s*(?!%s)\S)' % expr,
        pop=True
    )

def meta_set(scope):
    return [
        rule(meta_scope=scope),
        rule(clear_scopes=1),
        rule(match=r'', pop=True),
    ]

def expect_keyword(match, scope="keyword.other.sql", set_context=None):
    return expect(word(match), scope, set_context)

def expect_identifier(scope):
    return [
        rule(match=r'{{unquoted_identifier}}', scope=scope, pop=True),
        rule(
            match=r'(")([^"]+)(")',
            scope='string.quoted.double.sql',
            captures={
                '1': 'punctuation.definition.string.begin.sql',
                '2': scope,
                '3': 'punctuation.definition.string.end.sql',
            },
            pop=True,
        ),

        pop_unless(r'{{general_identifier}}'),
    ]
    
def expect_in_parens(contents):
    return [
        rule(
            match=r'\(',
            scope='punctuation.section.group.begin.sql',
            set=[
                expect(r'\)', 'punctuation.section.group.end.sql'),
                contents,
            ],
        ),
        rule(match=r'(?=\S)', pop=True),
    ]

def end(keyword=None):
    if bool(keyword):
        next_context = expect_keyword(keyword, 'keyword.control.sql')
    else:
        next_context = expect_identifier('variable.other.label.sql')

    return rule(
        match=word('END'),
        scope='keyword.control.sql',
        set=next_context,
    )

def word(match):
    return r'(?i)\b(?:%s)\b' % match

def word_ahead(match):
    return r'(?i)\b(?=(?:%s)\b)' % match

def empty_context(*args):
    return [ rule(match='', pop=True) ]

def all(*contexts):
    return [
        rule(include=context) for context in contexts
    ]

def heredoc(start, end):
    return rule(
        match=r"(?i)q\'%s" % start,
        scope='punctuation.definition.string.begin.sql',
        set=[
            rule(meta_include_prototype=False),
            rule(meta_scope='string.quoted.heredoc.sql'),
            rule(
                match=r"%s\'" % end,
                scope='punctuation.definition.string.end.sql',
                pop=True,
            ),
        ],
    )

def list_of(context):
    return [rule(
        match=r'',
        set=[
            [
                rule(
                    match=',',
                    scope='punctuation.separator.comma.sql',
                    push=context,
                ),
                rule(include='else-pop')
            ],
            context,
        ]
    )]
