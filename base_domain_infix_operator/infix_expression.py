#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from inspect import signature

from odoo.osv.expression import (
    AND_OPERATOR,
    NOT_OPERATOR,
    OR_OPERATOR,
    normalize_domain,
)

READABLE_NOT_OPERATOR = "NOT"
READABLE_AND_OPERATOR = "AND"
READABLE_OR_OPERATOR = "OR"


def _not_infix_term(term):
    return READABLE_NOT_OPERATOR, term


def _and_infix_term(first, second):
    return first, READABLE_AND_OPERATOR, second


def _or_infix_term(first, second):
    return first, READABLE_OR_OPERATOR, second


def to_infix_domain(prefix_domain):
    prefix_domain = normalize_domain(prefix_domain)
    op_to_func_dict = {
        NOT_OPERATOR: lambda l: _not_infix_term(l),
        AND_OPERATOR: lambda l1, l2: _and_infix_term(l1, l2),
        OR_OPERATOR: lambda l1, l2: _or_infix_term(l1, l2),
    }

    infix_domain = []
    for leaf in reversed(prefix_domain):
        infix_leaf_func = op_to_func_dict.get(leaf)
        if infix_leaf_func is not None:
            parameters = [
                infix_domain.pop() for _p in signature(infix_leaf_func).parameters
            ]
            infix_leaf = infix_leaf_func(*parameters)
        else:
            infix_leaf = leaf
        infix_domain.append(infix_leaf)
    return infix_domain
