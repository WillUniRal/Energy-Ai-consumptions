from datetime import date

date.fromisoformat()
date.isoformat()


class DEC :
    @property
    def date_today(self) -> date :
        return date.today()
    
    @property
    def year_begining(self) -> date :
        return date(self.date_today.year,1,1)

    def __init__(self,):
        pass
        
    def set_date(self,start_year,end_year) :
        self.start_date : date = date(start_year,1,1)
        self.end_date : date = date(end_year,12,31)

    def get_data(self) :
        pass