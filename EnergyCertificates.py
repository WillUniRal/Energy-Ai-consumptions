from datetime import date, timedelta

class Search :
    path = "/api/display/search"

    @property
    def date_today(self) -> date :
        return date.today()
    
    @property
    def constituency(self) -> tuple :
        return self.__constituency
    @property
    def postcode(self) -> tuple :
        return self.__postcode
    @property
    def address(self) -> tuple :
        return self.__address
    
    @constituency.setter
    def constituency(self,value) :
        self.__constituency = ("constituency[]",value)
    @postcode.setter
    def postcode(self,value) :
        self.__postcode = ("postcode",value)
    @address.setter
    def address(self,value) :
        self.__address = ("address",value)
    
    @property
    def params(self) -> dict :
        result : dict = {}

        if self.constituency : result |= dict([self.constituency])
        if self.postcode : result |= dict([self.postcode])
        if self.address : result |= dict([self.address])

        if not self.start_date : return result
        result["date_end"] = self.end_date.isoformat()
        result["date_start"] = self.start_date.isoformat()
        return result

    def __init__(self,):
        self.start_date : None|date = None
        self.__constituency = ()
        self.__postcode = ()
        self.__address = ()
        
    def set_date(self,start_year,end_year) :

        if end_year == self.date_today.year :
            end = self.date_today - timedelta(days=1)
        else : end = date(end_year,12,31)

        self.start_date : date = date(start_year,1,1)
        self.end_date : date = end

if __name__ == "__main__":
    
    apiParams = Search()
    print(apiParams.params)
    apiParams.set_date(2026,2026)
    print(apiParams.params)
    # {'date_start': '2026-01-01', 'date_end': '2026-06-08'}
