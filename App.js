import React from 'react'
import { Button, Input, Radio, Select, DatePicker } from 'antd'
import './App.css';
const App = () => {
  const data = [
    {'type': 'Text', 'content': '交通银行', 'px': '57px', 'py': '6px', 'width': '118px', 'height': '19px', 'fontsize': '17px', 'fontcolor': 'red'},
    {'type': 'Button', 'content': '工商银行', 'px': '198px', 'py': '8px', 'width': '260px', 'height': '15px', 'fontsize': '13px','backgroundcolor':'#0000FF', 'fontcolor': '#261002'},
    {'type': 'Input', 'content': '建设银行', 'px': '189px', 'py': '102px', 'width': '53px', 'height': '19px', 'fontsize': '17px', 'fontcolor': '#323636'},
    {'type': 'Radio', 'content': '中国银行', 'px': '19px', 'py': '62px', 'width': '53px', 'height': '19px', 'fontsize': '17px', 'fontcolor': '#323636'},
    {'type': 'Select', 'content': '农业银行', 'px': '259px', 'py': '32px', 'width': '53px', 'height': '19px', 'fontsize': '17px', 'fontcolor': '#323636'},
    {'type': 'DatePicker', 'content': '邮储银行', 'px': '369px', 'py': '202px', 'width': '53px', 'height': '19px', 'fontsize': '17px', 'fontcolor': '#323636'},
    ]

  return <div style={{ position: 'relative' }}>
    {data.map((item) => {
      const style =
      {
        position: 'absolute',
        left: item.px,
        top: item.py,
        width: item.width,
        height: item.height,
        fontSize: item.fontsize,
        color: item.fontcolor,
        backgroundColor:item.backgroundcolor

      }
      if (item.type === 'Text') return <text style={style}>{item.content}</text>
      if (item.type === 'Button') return <Button style={style}>{item.content}</Button>
      if (item.type === 'Radio') return <Radio style={style}>{item.content}</Radio>
      if (item.type === 'Input') return <Input style={style} placeholder={item.content} />
      if (item.type === 'Select') return <Select style={style} defaultValue={item.content} />
      if (item.type === 'DatePicker') return <DatePicker style={style}></DatePicker>
      return null;
    })}
  </div>


}
export default App;