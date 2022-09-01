class Lubleter():
    def __init__(self, name, entry_date, end_date, phone_number, price_range):
        self.name = name
        self.entry_date = entry_date
        self.end_date = end_date
        self.phone_number = phone_number
        self.price_range = price_range

    def __repr__(self):
        return f"{self.name}: {self.entry_date} - {self.end_date}"

    def __str__(self):
        range = " - ".join([date_str for date_str in [self.entry_date and f"desde {self.entry_date}",
                                                            self.end_date and f"hasta {self.end_date}"] if date_str])
        return f"{self.name}{f' ({self.phone_number})' if self.phone_number else ''} busca {range}"


class Looker(Lubleter):
    def fit(self, proposed_entry_date, proposed_end_date):
        return (self.entry_date <= proposed_entry_date <= self.end_date) or \
               (self.entry_date <= proposed_end_date <= self.end_date) \
               or (proposed_entry_date <= self.entry_date <= proposed_end_date) or (
                       proposed_entry_date <= self.end_date <= proposed_end_date)


class Offerer(Lubleter):
    def __init__(self, name, entry_date, end_date, phone_number, address, price_range, description):
        super().__init__(name, entry_date, end_date, phone_number, price_range)
        self.address = address
        self.description = description

    def opportunities(self, lookers):
        matches = []
        for looker in lookers:
            if looker.fit(self.entry_date, self.end_date):
                matches.append(str(looker))
        return ", ".join(matches)
