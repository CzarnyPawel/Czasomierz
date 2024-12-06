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
    • Framework: Django
    • Biblioteki: 

2. Instrukcje instalacji
Dostęp do repozytorium:
Należy użyć komendy: 
	git clone <do wklejenia adres z Git Hub>
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
(do uzupełnienia po stworzeniu aplikacji)

Funkcje specjalne
(Do opisania jeśli zostanie utworzony kalendarz oraz wysyłka powiadomień e-mail.)

4. FAQ (Najczęściej zadawane pytania)
1. Otrzymuję błąd przy próbie instalacji zależności. Dlaczego?
W przypadku, kiedy zostanie wyświetlony komunikat błędu, informujący, że któraś z zależności nie działa w sposób prawidłowy, należy samodzielnie uruchomić plik requirements.txt, jest to plik zapisany w notatniku systemowym, po czy przy wybranej zależności, która generuje problem usunąć numer wersji, następnie zapisać plik oraz ponownie wywołać komendę instalacji. Dzięki temu zainstalowana zostanie najnowsza możliwa wersja komponentu, który sprawiał problem.
2. Czy mogę zainstalować wirtualne środowisko bez użycia konsoli?
Tak. Instalacja wirtualnego środowiska możliwa jest również z poziomu IDE, z którego korzysta użytkownik. Aby zainstalować wirtualne środowisko (na przykładzie PyCharm) należy wybrać w prawym dolnym rogu IDE napis z wersją Pythona (na przykład: Python 3.10). W rozwiniętym menu kontekstowym wybrać opcję Add New Interpreter, następnie Add Local Interpreter, opcję Environment ustawić jako New wprowadzić lokalizację, w której utworzone zostanie wirtualne środowisko, opcję Base interpreter ustawić na Python 3.10, następnie wybrać przycisk OK. IDE utworzy wirtualne środowisko automatycznie.
3. Port 8000 wskazany w hiperłączu jest zajęty przez inne procesy w systemie, jak uruchomić aplikację?
W przypadku, gdy system aktualnie zajmuje port 8000 należy w konsoli wprowadzić:
	python manage.py runserver 8888, aby uruchomić aplikację np. na porcie 8888.

