import streamlit as st
from sqlalchemy import text

list_intention = ['', 'Baca Buku', 'Pinjam Buku', 'Belajar']

conn = st.connection("postgresql", type="sql", 
                     url="postgresql://nadia.2043221105:P4YglWGXSp3e@ep-muddy-rice-61227326.us-east-2.aws.neon.tech/web")
with conn.session as session:
    query = text('CREATE TABLE IF NOT EXISTS database_visitors (id serial, student_name text, student_id text, phone_number text, visit_date date, visit_time time, intention text, book_title text, book_code varchar(50));')
    session.execute(query)

st.header('DAFTAR KEHADIRAN RUANG BACA DEPARTEMEN STATISTIKA BISNIS')
page = st.sidebar.selectbox("Pilih Menu", ["View Data","Edit Data"])

if page == "View Data":
    data = conn.query('SELECT * FROM database_visitors ORDER By id;', ttl="0").set_index('id')
    st.dataframe(data)

if page == "Edit Data":
    if st.button('Tambah Data'):
        with conn.session as session:
            query = text('INSERT INTO database_visitors (student_name, student_id, phone_number, visit_date, visit_time, intention, book_title, book_code) \
                          VALUES (:1, :2, :3, :4, :5, :6, :7, :8);')
            session.execute(query, {'1':'', '2':'', '3':'', '4':None, '5':None, '6':'', '7':'', '8':''})
            session.commit()

    data = conn.query('SELECT * FROM database_visitors ORDER By id;', ttl="0")
    for _, result in data.iterrows():        
        id = result['id']
        student_name_lama = result["student_name"]
        student_id_lama = result["student_id"]
        phone_number_lama = result["phone_number"]
        visit_date_lama = result["visit_date"]
        visit_time_lama = result["visit_time"]
        intention_lama = result["intention"]
        book_title_lama = result["book_title"]
        book_code_lama = result["book_code"]

        with st.expander(f'a.n. {student_name_lama}'):
            with st.form(f'data-{id}'):
                student_name_baru = st.text_input("student_name", student_name_lama)
                student_id_baru = st.text_input("student_id", student_id_lama)
                phone_number_baru = st.text_input("phone_number", phone_number_lama)
                visit_date_baru = st.date_input("visit_date", visit_date_lama)
                visit_time_baru = st.time_input("visit_time", visit_time_lama)
                intention_baru = st.selectbox("intention", list_intention, list_intention.index(intention_lama))
                book_title_baru = st.text_input("book_title", book_title_lama)
                book_code_baru = st.text_input("book_code", book_code_lama)
                
                col1, col2 = st.columns([1, 6])

                with col1:
                    if st.form_submit_button('UPDATE'):
                        with conn.session as session:
                            query = text('UPDATE database_visitors \
                                          SET student_name=:1, student_id=:2, phone_number=:3, visit_date=:4, \
                                          visit_time=:5, intention=:6, book_title=:7, book_code=:8 \
                                          WHERE id=:9;')
                            session.execute(query, {'1':student_name_baru, '2':student_id_baru, '3':phone_number_baru, '4':(visit_date_baru), 
                                                    '5':visit_time_baru, '6':intention_baru, '7':book_title_baru, '8':book_code_baru, '9':id})
                            session.commit()
                            st.experimental_rerun()
                
                with col2:
                    if st.form_submit_button('DELETE'):
                        query = text(f'DELETE FROM database_visitors WHERE id=:1;')
                        session.execute(query, {'1':id})
                        session.commit()
                        st.experimental_rerun()
