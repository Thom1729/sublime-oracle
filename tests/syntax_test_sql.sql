-- SYNTAX TEST "Packages/Oracle/syntaxes/oracle-sql.sublime-syntax"

    select
--  ^^^^^^ meta.query.select keyword.other
        x
--      ^ meta.query.select variable.other
;

    select
    distinct
--  ^^^^^^^^ meta.query.select keyword.other
        x
--      ^ meta.query.select variable.other
;

    select
    all
--  ^^^ meta.query.select keyword.other
        x
--      ^ meta.query.select variable.other
;

    select
    unique
--  ^^^^^^ meta.query.select keyword.other
        x
--      ^ meta.query.select variable.other
;

    select
--  ^^^^^^^^ meta.query.select keyword.other
        x y
--      ^^^ meta.query.select meta.select-expression
--      ^ variable.other
--        ^ entity.name.alias
;

    select
--  ^^^^^^^^ meta.query.select keyword.other
        x as y
--      ^^^^^^ meta.query.select meta.select-expression
--      ^ variable.other
--        ^^ keyword.other
--           ^ entity.name.alias
;

    from
--  ^^^^ meta.query.from keyword.other
    t
--  ^ meta.query.from variable.other
;

    from
--  ^^^^ meta.query.from keyword.other
    t u
--  ^^^^ meta.query.from
--  ^ variable.other
--    ^ entity.name
;

    group
--  ^^^^^ meta.query.group_by keyword.other
    by
--  ^^ meta.query.group_by keyword.other

    x,
--  ^^^ meta.query.group_by
--  ^ variable.other
--   ^ punctuation.separator.comma

    rollup (x, y, z),
--  ^^^^^^^^^^^^^^^^^ meta.query.group_by
--  ^^^^^^ keyword.other
--          ^ variable.other

    cube (x, y, z),
--  ^^^^^^^^^^^^^^ meta.query.group_by
--  ^^^^ keyword.other
--        ^ variable.other

    grouping
--  ^^^^^^^^ meta.query.group_by keyword.other
    sets
--  ^^^^ meta.query.group_by keyword.other
    (
--  ^ meta.query.group_by punctuation.section.group.begin
        x,
--      ^^^ meta.query.group_by
--      ^ variable.other
--       ^ meta.query.group_by punctuation.separator.comma
    )
--  ^ meta.query.group_by punctuation.section.group.end
;
