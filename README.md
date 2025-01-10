# Czasomierz
Application for registration of working time and free time (holiday)

README (PL)
1. Opis projektu
Cel projektu: 
Projekt ma na celu zautomatyzowanie procesów związanych z rejestracją czasu pracy zdalnej, 
a także urlopami wypoczynkowymi, poprzez odejście od papierowej formy składania takich wniosków. Ponadto aplikacja ma na celu minimalizację błędów i nieścisłości wynikających 
z niewłaściwego wypełniania formularza papierowego. Aplikacja swoim charakterem zapewni również wsparcie przełożonym w skutecznym zarządzaniu, a także pracownikom w dostępie do danych związanych z historią swoich zgłoszeń.
Użyte technologie: 
    • Język programowania: Python 3.10 
    • Projekt opiera się głównie na funkcjonalnościach dostarczonych przez framework Django:
        ◦ Moduły do autoryzacji i uwierzytelniania: login, logout, LoginRequiredMixin, UserPassesTestMixin,
        ◦ Obsługa zapytań do bazy danych: Q,
        ◦ Obsługa odpowiedzi HTTP: HttpResponseRedirect,
        ◦ Skróty do przekierowań: redirect,
        ◦ Klasy widoków: View, TemplateView, CreateView, UpdateView, ListView, DeleteView, FormView,
        ◦ Obsługa URL: reverse_lazy, reverse.
    • Formularze – w projekcie zastosowano formularze, które zostały dostosowane do wymagań danego widoku, poprzez nadpisanie poszczególnych pól oraz zastosowanie odpowiednich etykiet czy widgetów.
    • W projekcie zastosowano następujące modele:
        ◦ User: nadpisany własnym modelem dziedziczącym po AbstractUser. W związku z tym zaktualizowano również ustawienia w pliku settings.py, aby wskazać Django, z jakiego domyślnego modelu powinno korzystać dodano zapis (AUTH_USER_MODEL),
        ◦ WorkLog: model obsługujący moduł rejestracji czasu pracy w projekcie. Obsługuje takie atrybuty jak:
            ▪ start_time: zawiera datę i czas rozpoczęcia pracy,
            ▪ end_time: zawiera datę i czas zakończenia pracy,
            ▪ tasks: opis wykonanych zadań, używany przy rejestracji zakończenia czasu pracy,
            ▪ state: stan aktywności logu pracy, domyślnie posiada status True. Status jest zmieniany na False w momencie złożenia wniosku o brak zdarzenia bądź korektę czasu pracy,
            ▪ name: nazwa logu. Domyślnie ma przypisaną wartość „Rejestracja czasu pracy”
            ▪ employee: przypisanie do użytkownika z usuwaniem kaskadowym.
        ◦ TeamUser: model łączący relacją wiele-do-wielu modele User oraz Team. Model posiada dodatkowe pole ‘role’, które opisuje stanowisko danego użytkownika w ramach przypisanego zespołu.
        ◦ Team: model obsługujący następujące atrybuty:
            ▪ name: nazwa zespołu, do którego może być przypisany użytkownik,
            ▪ description: zawiera opis zespołu.
        ◦ OffWorkLog: model obsługujący moduł urlopów w projekcie. Obsługuje takie atrybuty jak:
            ▪ start_date: zawiera datę rozpoczęcia urlopu,
            ▪ end_date: zawiera datę zakończenia urlopu,
            ▪ name: nazwa logu. Domyślnie ma przypisaną wartość „Urlop wypoczynkowy”
            ▪ status: zawiera status na jakim aktualnie znajduje się wniosek urlopowy,
            ▪ reason: zawiera opis w sytuacji, gdy akceptujący odrzuci złożony wniosek,
            ▪ employee: przypisanie do użytkownika z usuwaniem kaskadowym,
            ▪ amount_of_leave: przypisanie do modelu z określoną liczbą dni urlopu w danym roku wraz z usuwaniem kaskadowym.
        ◦ AmountOfLeave: model obsługujący przyznaną liczbę dni urlopowych danemu użytkownikowi w danym roku. Obsługuje takie atrybuty jak:
            ▪ year: zawiera rok do którego przypisana jest liczba dni urlopu,
            ▪ days_to_use: zawiera liczbę dni urlopu, z których może skorzystać użytkownik,
            ▪ employee: przypisanie do użytkownika z usuwaniem kaskadowym.
        ◦ UsedDays: model obsługujący wykorzystaną liczbę dni przez pracownika. Obsługuje następujące atrybuty:
            ▪ used_days: wykorzystana liczba dni,
            ▪ employee: przypisanie do użytkownika z usuwaniem kaskadowym.
    • Obsługa dat i czasu. Użyto biblioteki datetime i timedelta do manipulacji datami i czasem.
    • Obsługa e-maili: zastosowano EmailMultiAlternatives do wysyłania e-maili z systemu.
    • Kalendarz: wykorzystanie klasy Poland z biblioteki workalendar.europe do obsługi specyficznych dla Polski dni wolnych od pracy.


2. Instrukcje instalacji
Dostęp do repozytorium:
Należy użyć komendy: 
	SSH: git clone git@github.com:CzarnyPawel/Czasomierz.git
Po pomyślnym sklonowaniu repozytorium do lokalnego środowiska pracy, należy otworzyć projekt w IDE (na przykładzie PyCharm):
	File → Open → Należy wskazać główny katalog sklonowanej 			aplikacji
 bądź za pomocą  konsoli (jeśli znajduje się domyślnie w Katalogu domowym i również tam sklonował aplikację) przechodzi do katalogu z aplikacją używając komendy:
	cd <nazwa katalogu z aplikacją>
Konfiguracja wirtualnego środowiska:
Należy sprawdzić jaką wersję Pythona użytkownik ma zainstalowaną na swoim komputerze. W tym celu należy w konsoli wywołać komendę:
	python –version lub python3 –version
Jest to konieczne ponieważ w wersjach starszych niż 3.3 konieczna jest instalacja modułu venv.
W przypadku starszej wersji Pythona należy zainstalować dodatkowo następujący komponent:
	pip install virtualenv
Aby utworzyć wirtualne środowisko należy wprowadzić w konsoli następującą komendę:
python -m venv nazwa_środowiska lub python3 -m venv nazwa_środowiska
Po utworzeniu wirtualnego środowiska należy je jeszcze aktywować. Aktywacja wirtualnego środowiska zależy od systemu operacyjnego na jakim pracuje użytkownik. Należy wpisać jedną z następujących komend, znajdując się w konsoli w miejscu, gdzie dostępny jest folder z utworzonym powyżej wirtualnym środowiskiem:
Windows: 		nazwa_środowiska\Scripts\activate
Linux/MacOS: 	source nazwa_środowiska/bin/activate
Po pomyślnej instalacji i ponownym uruchomieniu terminala, obok ścieżki na której aktualnie znajduje się użytkownik powinna pojawić się nazwa utworzonego wirtualnego środowiska. Teraz można instalować dodatkowe komponenty, np. zależności opisane poniżej, dzięki czemu zainstalują się one tylko w obrębie aplikacji, z którą użytkownik pracuje a nie w ramach całego Pythona.
Dezaktywacja wirtualnego środowiska: 	deactivate
Instalacja zależności:
W tym celu należy wykorzystać dołączony do aplikacji plik requirements.txt. W konsoli należy przejść do katalogu głównego z aplikacją, następnie użyć komendy:
	pip install requirements.txt
Poprawna instalacja zależności zapewni, że zainstalowane zostaną wszystkie niezbędne biblioteki, które są wykorzystywane w systemie.
3. Instrukcje użycia
Podstawowe działanie
Aby rozpocząć korzystanie z projektu należy w konsoli przejść do katalogu głównego z aplikacją, gdzie znajduje się plik manage.py, i użyć komendy:
	python manage.py runserver
Następnie użytkownik wybiera dostępne w konsoli hiperłącze bądź samodzielnie wprowadza w pasku adresu przeglądarki internetowej adres:
	http://127.0.0.1:8000/
Utworzenie konta użytkownika
W systemie istnieje konto administracyjne. Domyślne dane logowania do tego konta to:
login: admin
hasło: admin 
Po poprawnym zalogowaniu do systemu zaleca się zmianę hasła domyślnego. Aby to uczynić, użytkownik wybiera link „Change password” dostępny w prawym górnym rogu panelu administracyjnego, prowadzący do zmiany hasła domyślnego. W pierwszym polu należy wprowadzić hasło domyślne, w dwóch kolejnych nowe hasło, które spełnia określone tam wymagania. Po poprawnym wygenerowaniu nowego hasła należy wybrać przycisk „Change my password”. 
Scenariusze użycia
1. Rejestracja rozpoczęcia i zakończenia czasu pracy
    • Użytkownik loguje się do systemu za pomocą przypisanego loginu i hasła
    • W aplikacji w menu w lewym górnym rogu należy wybrać zakładkę „Czas pracy”
    • W kolejnym oknie użytkownik wybiera kafelek „Rozpoczęcie pracy”
    • Po weryfikacji daty i godziny rozpoczęcia pracy użytkownik wybiera przycisk „Zarejestruj czas”, po poprawnej rejestracji czasu pracy zostaje przeniesiony do modułu „Czas pracy”
    • Użytkownik wybiera kafelek „Zakończenie pracy”
    • Po weryfikacji daty rozpoczęcia i zakończenia pracy należy jeszcze uzupełnić pole „zrealizowane zadania”, po czym wybrać przycisk „Zarejestruj czas”. Po poprawnej rejestracji zakończenia czasu pracy użytkownik zostaje przeniesiony do modułu „Czas pracy”.
2. Złożenie wniosku o korektę czasu pracy
    • Użytkownik loguje się do systemu za pomocą przypisanego loginu i hasła
    • W aplikacji w menu w lewym górnym rogu należy wybrać zakładkę „Czas pracy”
    • Użytkownik wybiera kafelek „Korekta czasu pracy”
    • Należy wpisać datę korekty czasu pracy. Na tej podstawie system w bazie odszuka stosowny rekord.
    • Użytkownikowi zostaje wyświetlony formularz, w którym za pomocą ikonki kalendarza ma możliwość skorygowania daty i godziny czasu pracy. 
    • Po dokonaniu korekty użytkownik wybiera przycisk „Wyślij wniosek”. Wniosek zostaje przesłany przełożonemu do akceptacji, jednocześnie wysyłając do niego wiadomość e-mail, iż taki wniosek oczekuje na akceptację.
3. Złożenie wniosku o brak zdarzenia
    • Użytkownik loguje się do systemu za pomocą przypisanego loginu i hasła
    • W aplikacji w menu w lewym górnym rogu należy wybrać zakładkę „Czas pracy”
    • Użytkownik wybiera kafelek „Brak zdarzenia”
    • W formularzu należy za pomocą ikony kalendarza wskazać datę i czas rozpoczęcia i zakończenia czasu pracy oraz uzupełnić pole „Zrealizowane zadania”. Po poprawnym uzupełnieniu formularza należy wybrać przycisk „Wyślij wniosek”. Wniosek zostaje przesłany przełożonemu do akceptacji, jednocześnie wysyłając do niego wiadomość e-mail, iż taki wniosek oczekuje na akceptację.
4. Raporty czasu pracy użytkownika oraz zatwierdzone wnioski
    • Użytkownik loguje się do systemu za pomocą przypisanego loginu i hasła
    • W aplikacji w menu w lewym górnym rogu należy wybrać zakładkę „Czas pracy”
    • Użytkownik wybiera kafelek „Raporty”
    • W formularzu należy uzupełnić zakres dat, dla których ma zostać wygenerowany raport czasu pracy, następnie wybrać przycisk „Pobierz dane”.
    • W nowym oknie prezentowane są godziny czasu pracy użytkownika we wskazanym wcześniej okresie. Wyświetlane są tylko zarejestrowane rekordy rozpoczęcia i zakończenia oraz zatwierdzone przez przełożonego wnioski o korektę oraz brak zdarzenia.
5. Akceptacja wniosków o korektę czasu pracy i brak zdarzenia
    • Użytkownik z rolą „team_lead” loguje się do systemu za pomocą przypisanego loginu i hasła
    • W aplikacji w menu w lewym górnym rogu należy wybrać zakładkę „Czas pracy”
    • Użytkownik wybiera kafelek „Akceptacje”
    • Wyświetlona zostaje lista wszystkich rekordów, które zostały przesłane do akceptacji, zawierając w kolumnie „Rodzaj wniosku” opis jakiego typu wniosek jest przesyłany. Użytkownik wybiera przycisk „Akceptuj” aby zaakceptować przesłany wniosek podległego pracownika.
6. Złożenie wniosku o urlop przez pracownika
    • Użytkownik loguje się do systemu za pomocą przypisanego loginu i hasła
    • W aplikacji w menu w lewym górnym rogu należy wybrać zakładkę „Urlopy”
    • Użytkownik wybiera kafelek „Wniosek urlopowy”
    • Użytkownik wskazuje w formularzu datę rozpoczęcia i zakończenia urlopu, po czym wybiera przycisk „Wyślij wniosek”. Wniosek zostaje przesłany przełożonemu do akceptacji, jednocześnie wysyłając do niego wiadomość e-mail, iż taki wniosek oczekuje na akceptację.
7. Raporty czasu pracy użytkownika oraz zatwierdzone wnioski
    • Użytkownik loguje się do systemu za pomocą przypisanego loginu i hasła
    • W aplikacji w menu w lewym górnym rogu należy wybrać zakładkę „Urlopy”
    • Użytkownik wybiera kafelek „Raporty”
    • W nowym oknie prezentowane są wszystkie złożone wnioski urlopowe wraz ze statusem jaki otrzymały w procesie akceptacji przez przełożonego.
8. Akceptacja wniosków urlopowych

    • Użytkownik z rolą „team_lead” loguje się do systemu za pomocą przypisanego loginu i hasła
    • W aplikacji w menu w lewym górnym rogu należy wybrać zakładkę „Urlopy”
    • Użytkownik wybiera kafelek „Akceptacje”
    • Wyświetlona zostaje lista wszystkich rekordów, które zostały przesłane do akceptacji. Użytkownik wybiera przycisk „Akceptuj” aby zaakceptować przesłany wniosek podległego pracownika.
Funkcje specjalne
1. Wysyłka wiadomości e-mail
Automatyczne informowanie przełożonego o nowych wnioskach o akceptację za pomocą funkcji EmailMultiAlternatives w Django. Zastosowano następujące rozwiązanie, aby w przypadku niepoprawnego przesłania wiadomości w standardowym formacie możliwe było jej wyświetlenie w formacie HTML.
2. Obliczanie dni urlopu
Wykorzystanie pakietu workalendar do precyzyjnego obliczania dni urlopu, które zostaną odjęte z puli pracownika po złożeniu wniosku wraz z uwzględnieniem dni roboczych i świątecznych. 

4. FAQ (Najczęściej zadawane pytania)
1. Otrzymuję błąd przy próbie instalacji zależności. Dlaczego?
W przypadku, kiedy zostanie wyświetlony komunikat błędu, informujący, że któraś z zależności nie działa w sposób prawidłowy, należy samodzielnie uruchomić plik requirements.txt, jest to plik zapisany w notatniku systemowym, po czy przy wybranej zależności, która generuje problem usunąć numer wersji, następnie zapisać plik oraz ponownie wywołać komendę instalacji. Dzięki temu zainstalowana zostanie najnowsza możliwa wersja komponentu, który sprawiał problem.
2. Czy mogę zainstalować wirtualne środowisko bez użycia konsoli?
Tak. Instalacja wirtualnego środowiska możliwa jest również z poziomu IDE, z którego korzysta użytkownik. Aby zainstalować wirtualne środowisko (na przykładzie PyCharm) należy wybrać w prawym dolnym rogu IDE napis z wersją Pythona (na przykład: Python 3.10). W rozwiniętym menu kontekstowym wybrać opcję Add New Interpreter, następnie Add Local Interpreter, opcję Environment ustawić jako New wprowadzić lokalizację, w której utworzone zostanie wirtualne środowisko, opcję Base interpreter ustawić na Python 3.10, następnie wybrać przycisk OK. IDE utworzy wirtualne środowisko automatycznie.
3. Port 8000 wskazany w hiperłączu jest zajęty przez inne procesy w systemie, jak uruchomić aplikację?
W przypadku, gdy system aktualnie zajmuje port 8000 należy w konsoli wprowadzić:
	python manage.py runserver 8888, aby uruchomić aplikację np. na porcie 8888.


README (EN)
1. Project description
Project goal: 
The project aims to automate processes related to recording remote working time, 
as well as holiday leaves, by moving away from the paper form of submitting such applications. Furthermore, the application aims to minimize resulting errors and inaccuracies from incorrectly filling out a paper form. The application's nature will also support superiors in effective management, as well as employees in access to data related to the history of their reports.

Technologies used: 
    • Programming language: Python 3.10 
    • The project is mainly based on functionalities provided by the Django framework:
        ◦ Authorization and authentication modules: login, logout, LoginRequiredMixin, UserPassesTestMixin,
        ◦ Database query support: Q,
        ◦ HTTP response support: HttpResponseRedirect,
        ◦ Redirection shortcuts: redirect,
        ◦ View classes: View, TemplateView, CreateView, UpdateView, ListView, DeleteView, FormView,
        ◦ URL support: reverse_lazy, reverse.
    • Forms – the project uses forms that have been adapted to the requirements of a given view by overwriting individual fields and using appropriate labels or widgets.
    • The following models were used in the project:
        ◦ User: overwritten with its own model inheriting from AbstractUser. As a result, the settings in the settings.py file have also been updated to indicate to Django what default model the added entry should use (AUTH_USER_MODEL),
        ◦ WorkLog: a model supporting the work time registration module in the project. Supports attributes such as:
            ▪ start_time: contains the date and time of starting work,
            ▪ end_time: contains the date and time when the work ended,
            ▪ tasks: description of completed tasks, used when recording the end of working time,
            ▪ state: activity status of the work log, by default it has the status True. The status is changed to False when you submit an application for no event or correction of working time,
            ▪ name: log name. By default, it is assigned the value "Working time registration"
            ▪ employee: user assignment with cascade deletion.
        ◦ TeamUser: a model connecting the User and Team models with a many-to-many relationship. The model has an additional 'role' field that describes the position of a given user within the assigned team.
        ◦ Team: a model that supports the following attributes:
            ▪ name: name of the team to which the user can be assigned,
            ▪ description: contains a description of the team.
        ◦ OffWorkLog: model supporting the leave module in the project. Supports attributes such as:
            ▪ start_date: contains the start date of the holiday,
            ▪ end_date: contains the end date of the holiday,
            ▪ name: log name. By default it is assigned the value "Vacation leave"
            ▪ status: contains the current status of the leave request,
            ▪ reason: contains a description in a situation where the acceptor rejects the submitted application,
            ▪ employee: user assignment with cascading deletion,
            ▪ amount_of_leave: assignment to a model with a specific number of leave days in a given year with cascading deletion.
        ◦ AmountOfLeave: a model that handles the number of vacation days allocated to a given user in a given year. Supports attributes such as:
            ▪ year: contains the year to which the number of vacation days is assigned,
            ▪ days_to_use: contains the number of vacation days that the user can use,
            ▪ employee: user assignment with cascade deletion.
        ◦ UsedDays: a model that handles the number of days used by an employee. Supports the following attributes:
            ▪ used_days: number of days used,
            ▪ employee: user assignment with cascade deletion.
    • Date and time support. Used datetime and timedelta libraries for date and time manipulation.
    • Email handling: EmailMultiAlternatives was used to send emails from the system.
    • Calendar: using the Poland class from the workalendar.europe library to handle non-working days specific to Poland.

2. Installation instructions
Repository access:
Use the command: 
        SSH: git clone git@github.com:CzarnyPawel/czasomierz.git
After successfully cloning the repository to your local work environment, open the project in the IDE (using PyCharm as an example):
        File → Open → Select the main directory of the cloned application
or using the console (if it is located in the Home directory by default and has also cloned the application there) goes to the directory with the application using the command:
        cd <application directory name>

Virtual environment configuration:
You should check what version of Python the user has installed on his computer. To do this, run the command in the console:
        python –version or python3 –version

This is necessary because in versions older than 3.3 it is necessary to install the venv module.
For an older version of Python, you must additionally install the following component:
        pip install virtualenv

To create a virtual environment, enter the following command in the console:
	python -m venv environment_name or python3 -m venv environment_name

After creating the virtual environment, you still need to activate it. Activation of the virtual environment depends on the operating system the user is running. Enter one of the following commands in the console where the folder with the virtual environment created above is available:
Windows: 		environment_name\Scripts\activate
Linux/MacOS: 	source environment_name/bin/activate
After successful installation and restart of the terminal, the name of the created virtual environment should appear next to the path where the user is currently located. Now you can install additional components, e.g. the dependencies described below, so that they will only install within the application you are working with and not within Python as a whole.

Deactivating the virtual environment: deactivate

Dependency installation:
For this purpose, use the requirements.txt file attached to the application. In the console, go to the main directory with the application, then use the command:
        pip install requirements.txt

Correct installation of dependencies will ensure that all necessary libraries that are used in the system are installed.

3. Instructions for use
Basic operation
To start using the project, go to the main application directory in the console, where the manage.py file is located, and use the command:
        python manage.py runserver

Then the user selects the hyperlink available in the console or enters the address in the address bar of the web browser:
        http://127.0.0.1:8000/

Creating a user account
There is an administrative account in the system. The default login details for this account are:

login: 		admin
password: 	admin
 
After successfully logging in to the system, it is recommended to change the default password. To do this, the user selects the "Change password" link available in the upper right corner of the administration panel, which leads to changing the default password. In the first field, enter the default password, and in the next two fields, enter a new password that meets the requirements specified there. After correctly generating a new password, select the "Change my password" button.

Usage scenarios
1. Registration of the start and end of working time
    • The user logs in to the system using the assigned login and password
    • In the application, in the menu in the upper left corner, select the "Working time" tab
    • In the next window, the user selects the "Getting started" tile
    • After verifying the date and time of work start, the user selects the "Record time" button, after correct registration of working time, he is transferred to the "Working time" module
    • User selects the "End of work" tile
    • After verifying the start and end date of work, complete the "completed tasks" field and select the "Record time" button. After correct registration of the end of working time, the user is transferred to the "Working time" module.

2. Submitting an application for correction of working time
    • The user logs in to the system using the assigned login and password
    • In the application, in the menu in the upper left corner, select the "Working time" tab
    • The user selects the "Working time correction" tile
    • Enter the working time correction date. Based on this, the system will find the appropriate record in the database.
    • A form is displayed to the user in which he or she can use the calendar icon to correct the date and working time. 
    • After making the correction, the user selects the "Send application" button. The application is sent to the supervisor for approval, and at the same time an e-mail is sent to him that the application is awaiting approval.

3. Submitting a no-event application
    • The user logs in to the system using the assigned login and password
    • In the application, in the menu in the upper left corner, select the "Working time" tab
    • User selects the "No event" tile
    • In the form, use the calendar icon to indicate the date and time of the start and end of working time and complete the "Completed tasks" field. After completing the form correctly, select the "Send application" button. The application is sent to the supervisor for approval, and at the same time an e-mail is sent to him that the application is awaiting approval.

4. User working time reports and approved applications
    • The user logs in to the system using the assigned login and password
    • In the application, in the menu in the upper left corner, select the "Working time" tab
    • User selects the "Reports" tile
    • In the form, complete the date range for which the working time report is to be generated, then select the "Download data" button.
    • The new window presents the user's working hours in the previously indicated period. Only registered start and end records and supervisor-approved correction requests and no events are displayed.

5. Acceptance of requests for correction of working time and no event
    • A user with the "team_lead" role logs in to the system using the assigned login and password
    • In the application, in the menu in the upper left corner, select the "Working time" tab
    • The user selects the "Acceptances" tile
    • A list of all records that have been submitted for approval is displayed, including a description of the type of request being submitted in the "Application Type" column. The user selects the "Accept" button to accept the submitted application of the subordinate employee.

6. Submitting an application for leave by the employee
    • The user logs in to the system using the assigned login and password
    • In the application, in the menu in the upper left corner, select the "Holidays" tab
    • The user selects the "Vacation request" tile
    • The user indicates the start and end date of the leave in the form and then selects the "Send application" button. The application is sent to the supervisor for approval, and at the same time an e-mail is sent to him that the application is awaiting approval.

7. User working time reports and approved applications
    • The user logs in to the system using the assigned login and password
    • In the application, in the menu in the upper left corner, select the "Holidays" tab
    • User selects the "Reports" tile
    • The new window presents all submitted leave applications along with the status they received in the process of approval by the superior.

8. Acceptance of leave requests
    • A user with the "team_lead" role logs in to the system using the assigned login and password
    • In the application, in the menu in the upper left corner, select the "Holidays" tab
    • The user selects the "Acceptances" tile
    • A list of all records that have been submitted for approval is displayed. The user selects the "Accept" button to accept the submitted application of the subordinate employee.

Special features
1. Sending e-mails
Automatically notify your manager of new approval requests using the EmailMultiAlternatives feature in Django. The following solution has been implemented so that if a message was sent incorrectly in the standard format, it could be displayed in HTML format.

2. Calculation of vacation days
Using the workalendar package to precisely calculate vacation days that will be deducted from the employee's pool after submitting the application, including working days and holidays.

4. FAQ (Frequently asked questions)
1. I get an error when trying to install dependencies. Why?
If an error message is displayed informing that one of the dependencies is not working properly, you should run the requirements.txt file yourself, this is a file saved in the system notebook, and then remove the version number from the selected dependency that generates the problem, then save the file and run the install command again. This will install the latest possible version of the component that caused the problem.

2. Can I install a virtual environment without using the console?
Yes. Installation of the virtual environment is also possible from the IDE level used by the user. To install the virtual environment (in the example of PyCharm), select the Python version in the lower right corner of the IDE (for example: Python 3.10). In the expanded context menu, select the Add New Interpreter option, then Add Local Interpreter, set the Environment option to New, enter the location where the virtual environment will be created, set the Base interpreter option to Python 3.10, then select the OK button. The IDE will create the virtual environment automatically.

3. Port 8000 indicated in the hyperlink is occupied by other processes in the system, how to run the application?
If the system currently occupies port 8000, enter the following in the console:
        python manage.py runserver 8888 to run the application, e.g. on port 8888.



