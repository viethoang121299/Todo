# Thu vien
import streamlit as st
import plotly.express as px
from datetime import datetime, date

# module tự viết
from database import init, add_tk, get_tk, get_tk_id, del_tk, upd_tk
from cloud import restore_db, backup_db

# Database
#restore_db()
init()

# Giao dien
st.set_page_config(page_title="Quản Lý Công Việc", layout="wide")
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Quản Lý Công Việc</h1>", unsafe_allow_html=True)
st.divider()

# Chia cac Tabs
tab1, tab2, tab3 = st.tabs(["Danh sách & Lọc", "Thêm mới", "Thống kê (Dashboard)"])

# Lấy dữ liệu


with tab1: # bai 4 sua tab nay
    df = get_tk()
    col_f1, col_f2 = st.columns(2)
    search = col_f1.text_input("🔍 Tìm tên việc")
    f_stat = col_f2.selectbox("Lọc trạng thái", ["Tất cả", "Chưa làm", "Đang làm", "Xong"])

    if search: df = df[df['name'].str.contains(search, case=False)]
    if f_stat != "Tất cả": df = df[df['status'] == f_stat]

    st.dataframe(df, use_container_width=True)
    st.download_button("📥 Tải CSV", df.to_csv(index=False).encode('utf-8-sig'), "tasks.csv", "text/csv")

    st.divider()
    st.subheader("Thao tác công việc")
    if not df.empty:
        tid = st.selectbox("Chọn ID", df['id'].tolist())
        t_data = get_tk_id(tid)
        t_edit, t_del = st.tabs(["Sửa", "Xóa"])

        with t_edit:
            with st.form("edit_f"):
                n_name = st.text_input("Tên việc", t_data[1])
                n_user = st.text_input("Phụ trách", t_data[4])
                # Ép kiểu date an toàn
                try:
                    d_val = datetime.strptime(t_data[3], '%Y-%m-%d').date()
                except:
                    d_val = date.today()
                n_dt = st.date_input("Hạn", d_val)
                n_stat = st.selectbox("Trạng thái", ["Chưa làm", "Đang làm", "Xong"],
                                      index=["Chưa làm", "Đang làm", "Xong"].index(t_data[2]))
                n_note = st.text_area("Ghi chú", t_data[5])

                if st.form_submit_button("Cập nhật"):
                    upd_tk(tid, n_name, n_stat, n_dt, n_user, n_note)
                    st.rerun()

        with t_del:
            if st.button("Xác nhận Xóa"):
                del_tk(tid)
                st.rerun()

with tab2:
    st.subheader("Tạo công việc mới:")
    with st.form('form_add'):
        c1, c2 = st.columns(2)
        name = c1.text_input('Tên công việc (*)')
        user = c1.text_input('Người phụ trách')
        dt = c2.date_input('Hạn chót', date.today())
        stat = c2.selectbox('Trạng thái', ['Chưa làm', 'Đang làm', 'Xong'])
        note = st.text_area('Ghi chú')

        if st.form_submit_button('Lưu Công Việc'):
            if name:
                add_tk(name, stat, dt, user, note)
                with st.spinner('Đang đồng bộ lên Google Drive...'):
                    backup_db()

                st.success('Đã lưu và đồng bộ dữ liệu thành công!')
                st.rerun()  # Cập nhật ngay lập tức
            else:
                st.error('Vui lòng nhập tên công việc!')

with tab3: #bai 4 them tab nay
    st.subheader("Phân tích hiệu suất")
    df = get_tk()
    if not df.empty:
        total = len(df)
        done = len(df[df['status'] == 'Xong'])
        doing = len(df[df['status'] == 'Đang làm'])

        # Dashboard mini
        col1, col2, col3 = st.columns(3)
        col1.metric("Tổng số việc", total)
        col2.metric("Đã hoàn thành", done, f"{(done / total) * 100:.0f}%" if total > 0 else "0%")
        col3.metric("Đang làm", doing)

        # Biểu đồ tròn
        fig = px.pie(df, names='status', title='Tỷ lệ Trạng thái Công việc', hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Chưa có dữ liệu.")

st.sidebar.write('SP được xây dựng bởi ...')
