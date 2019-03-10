"""
Unit tests for the linter helper functions and classes
"""
import slurmlint.linter as linter


def test_nodebank_undefined_errors():
    nb = linter.NodeBank()
    nb['cn1'].add_partition('prod', 13)
    nb['cn1'].add_partition('qa', 15)

    nb['cn2'].add_def(12)
    nb['cn2'].add_partition('prod', 14)


    nb['cn3'].add_partition('qa', 15)

    result = nb.undefined_node_errors()
    expected = [
        (13, 'Undefined nodes added to partition: cn1'),
        (15, 'Undefined nodes added to partition: cn1, cn3')
    ]
    assert result == expected


def test_nodebank_undefined_errors_ellipsis():
    nb = linter.NodeBank()
    nb['cn1'].add_partition('prod', 13)
    nb['ab1'].add_partition('prod', 13)
    nb['ac1'].add_partition('prod', 13)
    nb['ab3'].add_partition('prod', 13)

    result = nb.undefined_node_errors()
    expected = [
        (13, 'Undefined nodes added to partition: ab1, ab3, ac1, ...'),
    ]
    assert result == expected


def test_nodebank_duplicate_definition_errors():
    nb = linter.NodeBank()
    nb['cn1'].add_def(12)
    nb['cn2'].add_def(12)
    nb['cn2'].add_def(13)
    nb['cn3'].add_def(12)
    nb['cn3'].add_def(13)
    nb['cn3'].add_def(14)
    nb['cn4'].add_def(15)

    result = nb.duplicate_definition_errors()
    expected = [
        (12, 'Duplicate node definition: cn2, cn3'),
        (13, 'Duplicate node definition: cn2, cn3'),
        (14, 'Duplicate node definition: cn3')
    ]
    assert result == expected


def test_nodebank_duplicate_definition_errors_sameline():
    nb = linter.NodeBank()
    nb['cn1'].add_def(12)
    nb['cn1'].add_def(12)

    result = nb.duplicate_definition_errors()
    expected = [
        (12, 'Duplicate node definition: cn1'),
    ]
    assert result == expected


def test_nodebank_node_missing_partition_errors():
    nb = linter.NodeBank()
    nb['cn1'].add_def(11)
    nb['cn2'].add_def(11)
    nb['cn3'].add_def(12)
    nb['cn4'].add_def(12)
    nb['cn5'].add_def(12)
    nb['cn6'].add_def(12)
    nb['cn7'].add_def(12)
    nb['cn8'].add_def(12)

    nb['cn1'].add_partition('prod', 15)
    nb['cn4'].add_partition('prod', 15)

    result = nb.node_missing_partition_errors()
    expected = [
        (11, 'Defined node has no partition: cn2'),
        (12, 'Defined node has no partition: cn3, cn5, cn6, ...')
    ]
    assert result == expected
