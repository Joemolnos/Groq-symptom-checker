import groq

# Groq API beállítások
GROQ_API_KEY = "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"
GROQ_MODEL = "llama3-70b-8192"

# Groq kliens inicializálása
client = groq.Groq(api_key=GROQ_API_KEY)

# Szövegek és kérdések definíciója
SZOVEGEK = {
    "udvozles": "Üdvözöljük a Tünet Elemző Alkalmazásban!",
    "nem_kerdes": "Mi az Ön neme? (férfi/nő): ",
    "kor_kerdes": "Hány éves Ön? ",
    "terhes_kerdes": "Terhes Ön? (igen/nem): ",
    "elozmeny_kerdes": "Kérem, írja le röviden az egészségügyi előzményeit (pl. krónikus betegségek, műtétek, rendszeresen szedett gyógyszerek): ",
    "tunetek_kerdes": "Milyen tüneteket tapasztal jelenleg? Kérem, részletezze (pl. mióta állnak fenn, milyen súlyosságúak): ",
    "vizsgalat_kerdes": "Volt-e valamilyen orvosi vizsgálata nemrégiben? Ha igen, mi volt az eredménye? ",
    "labor_kerdes": "Végeztek-e Önnél laborvizsgálatokat? Ha igen, milyen eredményeket kapott? ",
    "elemzes_uzenet": "Elemzés folyamatban... Kérem, várjon.",
    "eredmeny_uzenet": "Eredmény:",
    "figyelmeztetes": "FIGYELMEZTETÉS:",
    "figyelmezteto_uzenet": "Ez az alkalmazás csak tájékoztató jellegű információkat nyújt, és nem helyettesíti az orvosi konzultációt. A pontos diagnózis felállításához és a megfelelő kezelés meghatározásához mindenképpen forduljon orvoshoz. Az itt kapott információkat beszélje meg kezelőorvosával.",
    "hiba_uzenet": "Hiba történt: {}",
    "szerver_hiba": "A szerver nem válaszol vagy túlterhelt... Kérjük, próbálja meg később."
}

def get_user_input(prompt):
    return input(prompt)

def groq_create(prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Ön egy segítőkész orvosi asszisztens, aki részletesen elemzi a kapott adatokat, és részletes tanácsokkat ad."},
            {"role": "user", "content": prompt}
        ],
        model=GROQ_MODEL,
    )
    return chat_completion.choices[0].message.content

def main():
    print(SZOVEGEK["udvozles"])
    
    nem = get_user_input(SZOVEGEK["nem_kerdes"])
    kor = get_user_input(SZOVEGEK["kor_kerdes"])
    terhes = "Nem" if nem.lower() == "férfi" else get_user_input(SZOVEGEK["terhes_kerdes"])
    
    elozmeny = get_user_input(SZOVEGEK["elozmeny_kerdes"])
    tunetek = get_user_input(SZOVEGEK["tunetek_kerdes"])
    vizsgalat = get_user_input(SZOVEGEK["vizsgalat_kerdes"])
    labor = get_user_input(SZOVEGEK["labor_kerdes"])

    prompt = f"""
    Ön egy {kor} éves {nem}. 
    Terhesség: {terhes}. 
    Kórelőzmény: {elozmeny}. 
    Jelenlegi tünetei: {tunetek}. 
    Fizikális vizsgálat eredményei: {vizsgalat}. 
    Laboreredmények: {labor}.

    Kérem, elemezze ezeket az információkat, és adjon részletes tájékoztatást a következőkről:
    1. Lehetséges diagnózisok (a legvalószínűbbekkel kezdve)
    2. Javasolt további vizsgálatok
    3. Lehetséges kezelési módok
    4. Várható lefolyás
    5. Tanácsok a beteg számára

    Kérem, a választ közérthető magyar nyelven fogalmazza meg, és részletesen kerülve a túlzottan szakmai kifejezéseket.
    """

    print(SZOVEGEK["elemzes_uzenet"])
    try:
        diagnostic = groq_create(prompt=prompt)
        print(SZOVEGEK["eredmeny_uzenet"])
        print(diagnostic)
    except Exception as e:
        print(SZOVEGEK["hiba_uzenet"].format(e))
        print(SZOVEGEK["szerver_hiba"])

    print("\n" + SZOVEGEK["figyelmeztetes"])
    print(SZOVEGEK["figyelmezteto_uzenet"])

if __name__ == "__main__":
    main()