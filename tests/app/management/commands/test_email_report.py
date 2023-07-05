from app.management.commands.email_report import Command


def test_email_report_returns_some_values():
    cm = Command()
    assert cm.handle() == 1


def test_email_report_does_not_return_some_values():
    cm = Command()
    assert cm.handle() != 2
