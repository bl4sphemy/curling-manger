import yagmail


class Emailer:
    # Attribute
    _sole_instance = None

    # Constructor
    def __init__(self, sender):
        if Emailer._sole_instance is None:
            self.sender_address = sender
            self.gmailer = yagmail.SMTP(sender)
            Emailer._sole_instance = self
        else:
            raise Exception("You cant create two Emailer classes")

    @classmethod
    def configure(cls, sender):
        cls.sender_address = sender
        cls.gmailer = yagmail.SMTP(sender)

    # return the only instance of this class
    @classmethod
    def instance(cls):
        if Emailer._sole_instance is None:
            cls.sender_address = ""
            Emailer._sole_instance = cls
        else:
            raise Exception("You can't' create two Emailer classes")

        return cls._sole_instance

    # send email
    def send_plain_email(self, recipients, subject, msg):
        for rec in recipients:
            self.gmailer.send(rec, subject, msg)


# main method for testing -> this works
if __name__ == "__main__":
    message = [
        'This is to test the instance and configure methods'
    ]
    e = Emailer('aether78@gmail.com')
    # e = Emailer.instance()
    # e.configure('ae@gmail.com')
    print(e.gmailer)
    print(e.sender_address)
    e.send_plain_email(['aether78@gmail.com'], 'Testing', message)
