from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')

old_script = '<script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>'
new_script = '<script src="https://cdn.jsdelivr.net/npm/exceljs@4.4.0/dist/exceljs.min.js"></script>'
if old_script in text:
    text = text.replace(old_script, new_script, 1)
elif 'exceljs.min.js' not in text:
    raise SystemExit('Excel library script tag not found')

new_export = r'''async function downloadInventoryExcel(){
  if(!latestInventory.matrix.length){alert('Keine Bestandsdaten zum Exportieren.');return}
  if(typeof ExcelJS==='undefined'){alert('Excel-Export konnte nicht geladen werden. Bitte die Seite neu laden.');return}
  try{
    const wb=new ExcelJS.Workbook();
    wb.creator='Tribeca Ice Cream';
    wb.created=new Date();
    const ws=wb.addWorksheet('Eisbestand',{properties:{defaultRowHeight:17}});
    const dateInfo=STORES.map(s=>`${s}: ${latestInventory.latest[s]||'–'}`).join(' · ');
    const dataRows=latestInventory.matrix.map(r=>[r.flavor,...STORES.map(s=>r.values[s]>0?r.values[s]:null),r.total]);
    const totalRow=5+dataRows.length;

    ws.mergeCells('A1:F1');
    ws.getCell('A1').value='Tribeca Ice Cream – aktueller Eisbestand';
    ws.getCell('A1').font={name:'Arial',size:15,bold:true,color:{argb:'FFFFFFFF'}};
    ws.getCell('A1').fill={type:'pattern',pattern:'solid',fgColor:{argb:'FF243447'}};
    ws.getCell('A1').alignment={vertical:'middle',horizontal:'left'};
    ws.getRow(1).height=25;

    ws.mergeCells('A2:F2');
    ws.getCell('A2').value=`Datenstand: ${dateInfo}`;
    ws.getCell('A2').font={name:'Arial',size:8,italic:true,color:{argb:'FF5B6573'}};
    ws.getCell('A2').alignment={vertical:'middle',horizontal:'left',wrapText:true};
    ws.getRow(2).height=22;
    ws.getRow(3).height=7;

    const headers=['Eissorte',...STORES,'Gesamt'];
    ws.addRow(headers);
    const header=ws.getRow(4);
    header.height=22;
    header.eachCell(cell=>{
      cell.font={name:'Arial',size:9,bold:true,color:{argb:'FF1F2937'}};
      cell.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FFC6F3E8'}};
      cell.alignment={vertical:'middle',horizontal:cell.col===1?'left':'center',wrapText:true};
      cell.border={bottom:{style:'medium',color:{argb:'FF101010'}}};
    });

    for(const rowData of dataRows){
      const row=ws.addRow(rowData);
      row.height=17;
      row.eachCell({includeEmpty:true},cell=>{
        cell.font={name:'Arial',size:9,color:{argb:'FF101010'}};
        cell.alignment={vertical:'middle',horizontal:cell.col===1?'left':'center'};
        cell.border={bottom:{style:'hair',color:{argb:'FFD9DEDC'}}};
      });
      for(let c=2;c<=6;c++){
        const cell=row.getCell(c);
        if(cell.value!==null&&cell.value!=='') cell.numFmt='0.0';
      }
      row.getCell(6).font={name:'Arial',size:9,bold:true,color:{argb:'FF101010'}};
      row.getCell(6).fill={type:'pattern',pattern:'solid',fgColor:{argb:'FFF0F7F5'}};
    }

    const totals=['Gesamt',...STORES.map(s=>latestInventory.totals[s]),latestInventory.grandTotal];
    const sumRow=ws.addRow(totals);
    sumRow.height=20;
    sumRow.eachCell(cell=>{
      cell.font={name:'Arial',size:9,bold:true,color:{argb:'FF101010'}};
      cell.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FFDCEFE7'}};
      cell.alignment={vertical:'middle',horizontal:cell.col===1?'left':'center'};
      cell.border={top:{style:'medium',color:{argb:'FF101010'}}};
      if(cell.col>1) cell.numFmt='0.0';
    });

    ws.columns=[
      {key:'flavor',width:27},
      {key:'pb',width:13},
      {key:'kb',width:11},
      {key:'fh',width:13},
      {key:'prod',width:11},
      {key:'total',width:10}
    ];
    ws.views=[{state:'frozen',ySplit:4,xSplit:0}];
    ws.autoFilter={from:'A4',to:`F${totalRow}`};
    ws.pageSetup={
      paperSize:9,
      orientation:'portrait',
      fitToPage:true,
      fitToWidth:1,
      fitToHeight:1,
      horizontalCentered:true,
      verticalCentered:false,
      margins:{left:0.2,right:0.2,top:0.3,bottom:0.3,header:0.1,footer:0.1},
      printArea:`A1:F${totalRow}`
    };
    ws.headerFooter={oddFooter:'&CSeite &P von &N'};

    const buffer=await wb.xlsx.writeBuffer();
    const blob=new Blob([buffer],{type:'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'});
    const url=URL.createObjectURL(blob),a=document.createElement('a');
    a.href=url;
    a.download=`Tribeca_Eisbestand_${todayBerlin()}.xlsx`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
  }catch(e){
    console.error(e);
    alert('Excel-Datei konnte nicht erstellt werden.');
  }
}
$('#downloadExcel').onclick=()=>downloadInventoryExcel();'''

pattern = re.compile(r"function downloadInventoryExcel\(\)\{.*?\}\n\$\('#downloadExcel'\)\.onclick=downloadInventoryExcel;", re.S)
text2, count = pattern.subn(new_export, text, count=1)
if count != 1:
    if 'async function downloadInventoryExcel()' in text and "$('#downloadExcel').onclick=()=>downloadInventoryExcel();" in text:
        text2 = text
    else:
        raise SystemExit(f'Export function replacement count was {count}')

path.write_text(text2, encoding='utf-8')
print('Patched Excel export formatting and A4 portrait print settings')
