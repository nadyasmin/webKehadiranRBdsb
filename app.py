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
            query = text('INSERT INTO database_visitors ("Name", "NRP", "Phone Number", "Visit Date", "Visit Time", "Intention", "Book Title", "Book Code") \
                          VALUES (:1, :2, :3, :4, :5, :6, :7, :8);')
            session.execute(query, {'1':'', '2':'', '3':'', '4':None, '5':None, '6':'', '7':'', '8':''})
            session.commit()

    data = conn.query('SELECT * FROM database_visitors ORDER By id;', ttl="0")
    for _, result in data.iterrows():        
        id = result['id']
        student_name_lama = result["Name"]
        student_id_lama = result["NRP"]
        phone_number_lama = result["Phone Number"]
        visit_date_lama = result["Visit Date"]
        visit_time_lama = result["Visit Time"]
        intention_lama = result["Intention"]
        book_title_lama = result["Book Title"]
        book_code_lama = result["Book Code"]

        with st.expander(f'a.n. {student_name_lama}'):
            with st.form(f'data-{id}'):
                student_name_baru = st.text_input("Name", student_name_lama)
                student_id_baru = st.text_input("NRP", student_id_lama)
                phone_number_baru = st.text_input("Phone Number", phone_number_lama)
                visit_date_baru = st.date_input("Visit Date", visit_date_lama)
                visit_time_baru = st.time_input("Visit Time", visit_time_lama)
                intention_baru = st.selectbox("Intention", list_intention, list_intention.index(intention_lama))
                book_title_baru = st.text_input("Book Title", book_title_lama)
                book_code_baru = st.text_input("Book Code", book_code_lama)
                
                col1, col2 = st.columns([1, 6])

                with col1:
                    if st.form_submit_button('UPDATE'):
                        with conn.session as session:
                            query = text('UPDATE database_visitors \
                                          SET "Name"=:1, "NRP"=:2, "Phone Number"=:3, "Visit Date"=:4, \
                                          "Visit Time"=:5, "Intention"=:6, "Book Title"=:7, "Book Code"=:8 \
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
