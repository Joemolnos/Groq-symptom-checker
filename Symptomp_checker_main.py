import streamlit as st
import groq

# Groq API beállítások
GROQ_API_KEY = "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"
GROQ_MODEL = "llama3-70b-8192"

# Groq kliens inicializálása
client = groq.Groq(api_key=GROQ_API_KEY)

# Szövegek és kérdések definíciója
SZOVEGEK = {
    "udvozles": "Üdvözöljük a Tünet Elemző Alkalmazásban!",
    "nem_kerdes": "Mi az Ön neme?",
    "kor_kerdes": "Hány éves Ön?",
    "terhes_kerdes": "Terhes Ön?",
    "elozmeny_kerdes": "Kérem, írja le röviden az egészségügyi előzményeit (pl. krónikus betegségek, műtétek, rendszeresen szedett gyógyszerek):",
    "tunetek_kerdes": "Milyen tüneteket tapasztal jelenleg? Kérem, részletezze (pl. mióta állnak fenn, milyen súlyosságúak):",
    "vizsgalat_kerdes": "Volt-e valamilyen orvosi vizsgálata nemrégiben? Ha igen, mi volt az eredménye?",
    "labor_kerdes": "Végeztek-e Önnél laborvizsgálatokat? Ha igen, milyen eredményeket kapott?",
    "elemzes_uzenet": "Elemzés folyamatban... Kérem, várjon.",
    "eredmeny_uzenet": "Eredmény:",
    "figyelmeztetes": "FIGYELMEZTETÉS:",
    "figyelmezteto_uzenet": "Ez az alkalmazás csak tájékoztató jellegű információkat nyújt, és nem helyettesíti az orvosi konzultációt. A pontos diagnózis felállításához és a megfelelő kezelés meghatározásához mindenképpen forduljon orvoshoz. Az itt kapott információkat beszélje meg kezelőorvosával.",
    "hiba_uzenet": "Hiba történt: {}",
    "szerver_hiba": "A szerver nem válaszol vagy túlterhelt... Kérjük, próbálja meg később."
}

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
    st.title("Tünet Elemző Alkalmazás")
    st.write(SZOVEGEK["udvozles"])
    
    nem = st.radio(SZOVEGEK["nem_kerdes"], options=["férfi", "nő"])
    kor = st.number_input(SZOVEGEK["kor_kerdes"], min_value=0, max_value=120, step=1)
    if nem == "nő":
        terhes = st.radio(SZOVEGEK["terhes_kerdes"], options=["igen", "nem"])
    else:
        terhes = "nem"
    
    elozmeny = st.text_area(SZOVEGEK["elozmeny_kerdes"])
    tunetek = st.text_area(SZOVEGEK["tunetek_kerdes"])
    vizsgalat = st.text_area(SZOVEGEK["vizsgalat_kerdes"])
    labor = st.text_area(SZOVEGEK["labor_kerdes"])
    
    if st.button("Elemzés indítása"):
        with st.spinner(SZOVEGEK["elemzes_uzenet"]):
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
            try:
                diagnostic = groq_create(prompt=prompt)
                st.success(SZOVEGEK["eredmeny_uzenet"])
                st.write(diagnostic)
            except Exception as e:
                st.error(SZOVEGEK["hiba_uzenet"].format(e))
                st.warning(SZOVEGEK["szerver_hiba"])

    st.write("\n" + SZOVEGEK["figyelmeztetes"])
    st.warning(SZOVEGEK["figyelmezteto_uzenet"])

if __name__ == "__main__":
    main()
