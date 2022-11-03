import './App.css';
import 'antd/dist/antd.min.css'
import { Button,Input,Select,Radio,DatePicker } from 'antd';
function App() {
  return (
    <div className="App">
      <div style={{position:'absolute',left:'57px',top:'7px',width:'118px',height:'18px',fontSize:'15px',color:'#D3C6B9'}}>6交通银行</div>
      <div style={{position:'absolute',left:'198px',top:'8px',width:'260px',height:'15px',fontSize:'7px',color:'#261002'}}>[UAT】定制查询（06002088)[FDASBS0101]</div>
      <div style={{position:'absolute',left:'916px',top:'4px',width:'202px',height:'21px',fontSize:'15px',color:'#1A0C01'}}>263M待逾0</div>
      <div style={{position:'absolute',left:'1211px',top:'7px',width:'123px',height:'17px',fontSize:'15px',color:'#A9C3D1'}}>14:400</div>
      <div style={{position:'absolute',left:'193px',top:'68px',width:'202px',height:'18px',fontSize:'11px',color:'#464746'}}>国结业务>定制查询>自定义查询</div>
      <div style={{position:'absolute',left:'188px',top:'102px',width:'67px',height:'19px',fontSize:'9px',color:'#3A3C39'}}>自定义查询</div>
      <div style={{position:'absolute',left:'415px',top:'145px',width:'125px',height:'19px',fontSize:'10px',color:'#3B2F98'}}>重新开始定义一个查询</div>
      <div style={{position:'absolute',left:'417px',top:'183px',width:'216px',height:'14px',fontSize:'10px',color:'#2D2892'}}>选择已经定义好的查询并进行修改或扩展</div>
      <div style={{position:'absolute',left:'415px',top:'216px',width:'124px',height:'20px',fontSize:'10px',color:'#382BA7'}}>共享其他机构查询模板</div>
      <div style={{position:'absolute',left:'17px',top:'736px',width:'90px',height:'20px',fontSize:'10px',color:'#160501'}}>用户名：张喜妹</div>
      <div style={{position:'absolute',left:'289px',top:'736px',width:'98px',height:'15px',fontSize:'7px',color:'#140600'}}>用户号：3152407</div>
      <div style={{position:'absolute',left:'559px',top:'737px',width:'123px',height:'19px',fontSize:'10px',color:'#220D02'}}>机构名称：业务管理部</div>
      <div style={{position:'absolute',left:'827px',top:'734px',width:'144px',height:'22px',fontSize:'8px',color:'#CDC4BB'}}>机构代码：01315600010</div>
      <div style={{position:'absolute',left:'1098px',top:'734px',width:'138px',height:'22px',fontSize:'8px',color:'#CDC3B7'}}>会计日期：2069-04-05</div>
      <Button style={{position:'absolute',left:'1074px',top:'646px',width:'116px',height:'53px',fontSize:'17px',backgroundColor:'#EEB047',color:'#8E6E35'}}>下一步</Button>
      <Radio style={{position:'absolute',left:'207px',top:'142px',width:'86px',height:'25px',fontSize:'12px',color:'#56452B'}}>新建查询</Radio>
      <Radio style={{position:'absolute',left:'209px',top:'179px',width:'108px',height:'24px',fontSize:'10px',color:'#483F35'}}>○引用查询模板</Radio>
      <Radio style={{position:'absolute',left:'209px',top:'217px',width:'108px',height:'20px',fontSize:'10px',color:'#544832'}}>O共享查询模板</Radio>
    </div>
  );
}
export default App;