import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, ColumnsAutoSizeMode
from st_aggrid.shared import JsCode

st.set_page_config(layout='wide')

col_name = {
    'str_bid_num': 'ลำดับที่การขาย',
    'rai': 'ไร่',
    'quaterrai': 'งาน',
    'wa': 'วา',
    'biddate1': 'วันประมูลที่ 1',
    'biddate2': 'วันประมูลที่ 2',
    'biddate3': 'วันประมูลที่ 3',
    'biddate4': 'วันประมูลที่ 4',
    'biddate5': 'วันประมูลที่ 5',
    'biddate6': 'วันประมูลที่ 6',
    'biddate7': 'วันประมูลที่ 7',
    'biddate8': 'วันประมูลที่ 8',
    'landpicture': 'รูปทรัพย์',
    'map': 'แผนที่',
    'is_extra_pledgb': None,
    'owner_suit_name': 'เจ้าของสำนวน',
    'occupant': None,
    'assettypedesc': 'ประเภททรัพย์',
    'AssetTypeID': None,
    'addrno': 'เลขที่',
    'tumbol': None,
    'ampur': None,
    'city': None,
    'fbidnum': None,
    'fbidnuml': None,
    'fsubbidnum': None,
    'issale': None,
    'law_court_name': 'ศาล',
    'law_court_id': None,
    'law_suit_no': 'หมายเลขคดี',
    'law_suit_year': 'ปีคดี',
    'person1': 'โจทก์',
    'person2': 'จำเลย',
    'province_name': 'ติดต่อ',
    'province_id': None,
    'auc_asset_gen': None,
    'tel': 'โทรศัพท์',
    'debtdetail': None,
    'eauc': None,
    'remark1': None,
    'ReserveFund': 'หลักประกัน (ผู้ประสงค์จะเข้าเสนอราคา)',
    'ReserveFund1': 'หลักประกัน (ผู้มีสิทธิหักส่วนได้ใช้แทนหรือคู่สมรสที่ศาลมีคำสั่งอนุญาตให้กันส่วนแล้ว)',
    'assetprice1': None,
    'assetprice2': None,
    'assetprice3': 'ราคาประเมินของเจ้าพนักงานบังคับคดี',
    'assetprice4': None,
    'assetprice5': None,
    'assetprice6': None,
    'assetprice7': None,
    'assetprice8': None,
    'assetprice9': None,
    'ischeck_date': 'วันที่ประกาศขึ้นเว็บ',
    'remark': 'หมายเหตุ',
    'deedno': 'โฉนดเลขที่',  # landtype deedno
    'deedtumbol': 'แขวง/ตำบล',
    'deedampur': 'เขต/อำเภอ',
    'deedcity': 'จังหวัด',
    'landtype': None,  # landtype deedno
    'landdesc': None,
    'issale1': None,
    'issale2': None,
    'issale3': None,
    'issale4': None,
    'issale5': None,
    'issale6': None,
    'issale7': None,
    'issale8': None,
    'ownername': None,
    'saletypename': 'จะทำการขายโดย',
    'sale_location1': 'สถานที่จำหน่าย',
    'sale_location2': None,
    'sale_time1': 'เวลาจำหน่าย',
    'sale_time2': None,
    'debtname': None,
    'debtprice': None,
    'mapjot': 'แผนที่โจทก์ส่ง'
}

original_columns = [v if v is not None else k for k, v in col_name.items()]


@st.cache_data
def get_data():
    df_ = pd.read_csv('output.csv')
    for col in df_.columns:
        if 'date' in col:
            notna_idx = df_[col].notna()
            if len(notna_idx) > 0:
                df_.loc[notna_idx, col] = df_.loc[notna_idx, col] - 5430000

                #df_[col] = df_[col].str[:4] + '-' + df_[col].str[4:6] + '-' + df_[col].str[6:8]
                #yyyy = df_.loc[notna_idx, col].str[:4].astype(int, errors='ignore') - 543
                #yyyy = yyyy.astype(str)

                # df_.loc[notna_idx, col] = df_.loc[notna_idx, col].astype(str)
                # df_.loc[notna_idx, col] = df_.loc[notna_idx, col].str[6:8] + '-' + df_.loc[notna_idx, col].str[4:6] + '-' + df_.loc[notna_idx, col].str[:4]
                # df_.loc[notna_idx, col] = pd.to_datetime(df_.loc[notna_idx, col], format='%d-%m-%Y', errors='coerce')

                df_[col] = df_[col].astype(str)
                df_[col] = df_[col].str[6:8] + '-' + df_.loc[notna_idx, col].str[4:6] + '-' + df_.loc[notna_idx, col].str[:4]
                df_[col] = pd.to_datetime(df_[col], format='%d-%m-%Y', errors='coerce')
                #df_[col] = df_[col].dt.strftime('%d-%m-%Y')
    df_.columns = original_columns
    df_.insert(1, 'บันทึก', '')
    df_.insert(1, 'สถานะ', '')
    return df_


df = get_data()

# new_columns = st.sidebar.multiselect("คอลัมน์", original_columns, default=original_columns)
# hide_columns = [col for col in original_columns if col not in new_columns]


gb = GridOptionsBuilder.from_dataframe(df, editable=True)
url2img = JsCode("""
        class UrlCellRenderer {
          init(params) {
            this.eGui = document.createElement('img');
            this.eGui.setAttribute('src', params.value);
            this.eGui.setAttribute('width', 100);
          }
          getGui() {
            return this.eGui;
          }
        }
    """)

mouseover_popup_img = JsCode("""
        class UrlCellRenderer {
            init(params) {
                this.eGui = document.createElement('div');
                this.eGui.style.display = 'flex';
                this.eGui.style.alignItems = 'center';
                
                const img = document.createElement('img');
                img.src = params.value;
                img.style.maxWidth = '100px';
                img.style.height = 'auto';
                img.style.cursor = 'pointer';
                
                let popup = null;
                
                img.addEventListener('mouseover', (event) => {{
                    popup = document.createElement('div');
                    popup.style.position = 'absolute';
                    popup.style.zIndex = '10';
                    popup.style.border = '1px solid #ccc';
                    popup.style.boxShadow = '2px 2px 5px rgba(0,0,0,0.3)';
                    popup.style.backgroundColor = 'white';
                    popup.style.padding = '5px';
                    
                    const originalImg = document.createElement('img');
                    originalImg.src = params.value;
                    originalImg.style.maxWidth = '200px';
                    popup.appendChild(originalImg);
                    document.body.appendChild(popup);
                    
                    const rect = event.target.getBoundingClientRect();
                    const popup_width = popup.offsetWidth;
                    popup.style.left = (rect.left-popup_width) + 'px';
                    popup.style.top = rect.top + 'px';
                }});
                
                img.addEventListener('mouseout', () => {{
                    if (popup) {{
                        document.body.removeChild(popup);
                        popup = null;
                    }}
                }});
                
                this.eGui.appendChild(img);
            }
            getGui() {
                return this.eGui;
            }
        }
    """)

mouseover_resize_img = JsCode("""
        class UrlCellRenderer {
            init(params) {
                this.eGui = document.createElement('div');
                this.eGui.style.display = 'flex';
                this.eGui.style.alignItems = 'center';

                const img = document.createElement('img');
                img.src = params.value;
                img.style.maxWidth = '100px';
                img.style.height = 'auto';
                img.style.cursor = 'pointer';


                img.addEventListener('mouseover', (event) => {{
                    img.style.maxWidth = '200px';
                    img.style.height = 'auto';
                }});

                img.addEventListener('mouseout', () => {{
                    if (img.style.maxWidth == '200px') {{
                        img.style.maxWidth = '100px';
                        img.style.height = 'auto';
                    }}
                }});

                this.eGui.appendChild(img);
            }
            getGui() {
                return this.eGui;
            }
        }
    """)

mouseclick_full_img = JsCode("""
        class UrlCellRenderer {
            init(params) {
                this.eGui = document.createElement('div');
                this.eGui.style.display = 'flex';
                this.eGui.style.alignItems = 'center';

                const img = document.createElement('img');
                img.src = params.value;
                img.style.maxWidth = '100px';
                img.style.height = 'auto';
                img.style.cursor = 'pointer';

                let popup = null;
                
                img.addEventListener('click', (event) => {{
                    popup = document.createElement('div');
                    popup.style.display = 'block';
                    popup.style.position = 'fixed';
                    popup.style.zIndex = '1';
                    popup.style.paddingTop = '100px';
                    popup.style.left = '0';
                    popup.style.top = '0';
                    popup.style.width = '100%';
                    popup.style.height = '100%';
                    popup.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
                    popup.style.overflow = 'auto';

                    const originalImg = document.createElement('img');
                    originalImg.src = params.value;
                    originalImg.style.margin = 'auto';
                    originalImg.style.display = 'block';
                    originalImg.style.width = '100%';
                    originalImg.style.maxWidth = '500px';
                    originalImg.style.cursor = 'pointer';
                    originalImg.setAttribute('title', 'เปิดภาพในแท็บใหม่');
                    
                    const close_button = document.createElement('span');
                    close_button.style.position = 'absolute';
                    close_button.style.top = '15px';
                    close_button.style.right = '35px';
                    close_button.style.color = 'white';
                    close_button.style.fontSize = '40px';
                    close_button.style.fontWeight = 'bold';
                    close_button.style.cursor = 'pointer';
                    close_button.innerHTML = '&times;';
                    close_button.setAttribute('title', 'ปิด');
                                        
                    popup.appendChild(close_button);
                    popup.appendChild(originalImg);
                    document.body.appendChild(popup);
                    
                    originalImg.addEventListener('click', () => {{
                        window.open(params.value, 'Image');
                    }});
                    
                    close_button.addEventListener('click', () => {{
                        document.body.removeChild(popup);
                        popup = null;
                    }});

                }});



                this.eGui.appendChild(img);
            }
            getGui() {
                return this.eGui;
            }
        }
    """)

gb.configure_column(
    col_name['map'],
    headerName=col_name['map'],
    cellRenderer=mouseclick_full_img
)
gb.configure_column(
    col_name["landpicture"],
    headerName=col_name["landpicture"],
    cellRenderer=mouseclick_full_img
)
gb.configure_column(
    col_name["mapjot"],
    headerName=col_name["mapjot"],
    cellRenderer=mouseclick_full_img,
)
gb.configure_column(
    'สถานะ',
    headerName='สถานะ',
    cellEditor='agSelectCellEditor',
    cellEditorParams={'values': ['ขายแล้ว', 'สู้', 'ไม่สู้', 'ชนะ', 'แพ้', 'ไม่สนใจ']}
)
gb.configure_column(
    'บันทึก',
    headerName='บันทึก',
    cellEditor='agLargeTextCellEditor',
    warpText=True,
    autoHeight=True,
    cellEditorPopup=True
)
gb.configure_grid_options(
    rowHeight=100  # Enable auto row height
)
gb.configure_pagination(enabled=True)

for column in df.columns:
    print(df[column].dtype)
    if df[column].dtype == 'datetime64[ns]':
    #if column == 'วันประมูลที่ 1':
        gb.configure_column(column,
                            filter='agDateColumnFilter',
                            #valueFormatter={'function': "d3.timeFormat('%d-%m-%Y')(value)"},
                            #type=['customDateTimeFormat'],
                            #custom_format_string='yyyy-MM-dd'
                            )
    else:
        gb.configure_column(column, filter=True)

GB = gb.build()



# for col in GB["columnDefs"]:
#     if col["headerName"] in hide_columns:
#         col["hide"] = True


grid = AgGrid(df,
            gridOptions=GB,
            updateMode=GridUpdateMode.VALUE_CHANGED,
            height=700,
            warpText=True,
            columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
            allow_unsafe_jscode=True)


