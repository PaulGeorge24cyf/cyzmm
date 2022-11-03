import './App.css';
import 'antd/dist/antd.min.css'
import { Button,Input,Select,Radio,DatePicker } from 'antd';
function App() {
  return (
    <div className="App">
      <div style={{position:'absolute',left:'57px',top:'6px',width:'118px',height:'19px',fontSize:'15px',color:'#D3C5B9'}}>6交通银行</div>
      <div style={{position:'absolute',left:'198px',top:'8px',width:'260px',height:'15px',fontSize:'7px',color:'#261002'}}>[UAT】定制查询（06002088)[FDASBS0101]</div>
      <div style={{position:'absolute',left:'189px',top:'102px',width:'53px',height:'19px',fontSize:'8px',color:'#323636'}}>查询条件</div>
      <div style={{position:'absolute',left:'303px',top:'149px',width:'61px',height:'20px',fontSize:'7px',color:'#453F3C'}}>同比/环比：</div>
      <div style={{position:'absolute',left:'746px',top:'152px',width:'80px',height:'16px',fontSize:'10px',color:'#2E2C2A'}}>显示项目类型</div>
      <div style={{position:'absolute',left:'284px',top:'188px',width:'79px',height:'15px',fontSize:'8px',color:'#45413D'}}>业务当前状态：</div>
      <div style={{position:'absolute',left:'749px',top:'189px',width:'77px',height:'15px',fontSize:'8px',color:'#9A9491'}}>收益汇总项目：</div>
      <div style={{position:'absolute',left:'300px',top:'223px',width:'60px',height:'20px',fontSize:'8px',color:'#3F3B37'}}>开始时间：</div>
      <div style={{position:'absolute',left:'774px',top:'224px',width:'56px',height:'16px',fontSize:'8px',color:'#646160'}}>结束时间：</div>
      <div style={{position:'absolute',left:'287px',top:'258px',width:'70px',height:'20px',fontSize:'8px',color:'#423B4B'}}>*发起渠道：</div>
      <div style={{position:'absolute',left:'756px',top:'256px',width:'73px',height:'23px',fontSize:'9px',color:'#4E484F'}}>★客户等级：</div>
      <div style={{position:'absolute',left:'236px',top:'296px',width:'124px',height:'14px',fontSize:'10px',color:'#423F3B'}}>*是否跨境人民市业务</div>
      <div style={{position:'absolute',left:'759px',top:'296px',width:'69px',height:'16px',fontSize:'8px',color:'#37322E'}}>*是否代理：</div>
      <div style={{position:'absolute',left:'276px',top:'333px',width:'77px',height:'15px',fontSize:'8px',color:'#42403D'}}>交易对手编号：</div>
      <div style={{position:'absolute',left:'748px',top:'333px',width:'78px',height:'15px',fontSize:'8px',color:'#413E3B'}}>交易对手名址：</div>
      <div style={{position:'absolute',left:'281px',top:'355px',width:'79px',height:'23px',fontSize:'9px',color:'#46423E'}}>交易对手银行</div>
      <div style={{position:'absolute',left:'732px',top:'360px',width:'98px',height:'15px',fontSize:'9px',color:'#433F3A'}}>交易对手银行同业</div>
      <div style={{position:'absolute',left:'311px',top:'372px',width:'49px',height:'20px',fontSize:'6px',color:'#3D3A36'}}>SWIFT:</div>
      <div style={{position:'absolute',left:'789px',top:'375px',width:'41px',height:'16px',fontSize:'6px',color:'#2E312E'}}>客户号：</div>
      <div style={{position:'absolute',left:'262px',top:'405px',width:'93px',height:'15px',fontSize:'7px',color:'#453E3B'}}>联动银行SWIFT：</div>
      <div style={{position:'absolute',left:'734px',top:'396px',width:'96px',height:'16px',fontSize:'9px',color:'#292C28'}}>联动银行同业客户</div>
      <div style={{position:'absolute',left:'299px',top:'438px',width:'58px',height:'20px',fontSize:'8px',color:'#3C3934'}}>商品类别：</div>
      <div style={{position:'absolute',left:'772px',top:'438px',width:'57px',height:'20px',fontSize:'8px',color:'#3C3832'}}>商品编号：</div>
      <div style={{position:'absolute',left:'314px',top:'474px',width:'47px',height:'19px',fontSize:'7px',color:'#403E3D'}}>*币种：</div>
      <div style={{position:'absolute',left:'774px',top:'477px',width:'54px',height:'15px',fontSize:'7px',color:'#3F3C37'}}>商品名称：</div>
      <div style={{position:'absolute',left:'267px',top:'513px',width:'91px',height:'14px',fontSize:'8px',color:'#3E3A37'}}>金额区间FROM:</div>
      <div style={{position:'absolute',left:'756px',top:'510px',width:'73px',height:'19px',fontSize:'8px',color:'#3C3732'}}>金额区间TO：</div>
      <div style={{position:'absolute',left:'278px',top:'544px',width:'83px',height:'23px',fontSize:'9px',color:'#4A4542'}}>优惠费用标志：</div>
      <div style={{position:'absolute',left:'756px',top:'544px',width:'73px',height:'23px',fontSize:'9px',color:'#4B474B'}}>*是否上收：</div>
      <div style={{position:'absolute',left:'277px',top:'584px',width:'78px',height:'15px',fontSize:'8px',color:'#403D3B'}}>同业属性信息：</div>
      <div style={{position:'absolute',left:'735px',top:'581px',width:'94px',height:'23px',fontSize:'9px',color:'#4C474B'}}>*地区创新标志：</div>
      <div style={{position:'absolute',left:'276px',top:'620px',width:'78px',height:'16px',fontSize:'8px',color:'#2C2C29'}}>是否联动业务：</div>
      <div style={{position:'absolute',left:'759px',top:'620px',width:'67px',height:'16px',fontSize:'8px',color:'#2C2E2F'}}>*企业规模：</div>
      <div style={{position:'absolute',left:'289px',top:'657px',width:'68px',height:'16px',fontSize:'8px',color:'#37343C'}}>*离岸标志：</div>
      <div style={{position:'absolute',left:'239px',top:'688px',width:'559px',height:'18px',fontSize:'15px',color:'#4E331F'}}>汇总查询时下述查询条件可作为维度显示在汇总查询结果的首列或次列</div>
      <div style={{position:'absolute',left:'18px',top:'736px',width:'89px',height:'20px',fontSize:'9px',color:'#160500'}}>用户名：张喜妹</div>
      <div style={{position:'absolute',left:'286px',top:'733px',width:'102px',height:'23px',fontSize:'7px',color:'#D0C4BA'}}>用户号：3152407</div>
      <div style={{position:'absolute',left:'559px',top:'736px',width:'123px',height:'20px',fontSize:'10px',color:'#1F0B02'}}>机构名称：业务管理部</div>
      <div style={{position:'absolute',left:'829px',top:'736px',width:'141px',height:'18px',fontSize:'7px',color:'#120601'}}>机构代码：01315600010</div>
      <div style={{position:'absolute',left:'1098px',top:'734px',width:'138px',height:'22px',fontSize:'8px',color:'#CEC3B8'}}>会计日期：2069-04-05</div>
      <Input style={{position:'absolute',left:'838px',top:'252px',width:'293px',height:'27px',fontSize:'22px',color:'#5B5C5C'}} placeholder="全部"/>
      <Input style={{position:'absolute',left:'375px',top:'288px',width:'289px',height:'27px',fontSize:'22px',color:'#363636'}} placeholder="全部"/>
      <Input style={{position:'absolute',left:'839px',top:'288px',width:'290px',height:'27px',fontSize:'22px',color:'#353535'}} placeholder="全部"/>
      <Input style={{position:'absolute',left:'367px',top:'324px',width:'295px',height:'27px',fontSize:'22px',color:'#3B3B37'}} placeholder="全部"/>
      <Input style={{position:'absolute',left:'837px',top:'324px',width:'297px',height:'27px',fontSize:'22px',color:'#3C3B37'}} placeholder="全部"/>
      <Input style={{position:'absolute',left:'367px',top:'360px',width:'274px',height:'27px',fontSize:'22px',color:'#343331'}} placeholder="全部"/>
      <Input style={{position:'absolute',left:'839px',top:'360px',width:'274px',height:'27px',fontSize:'22px',color:'#353435'}} placeholder="全部"/>
      <Input style={{position:'absolute',left:'367px',top:'396px',width:'274px',height:'27px',fontSize:'22px',color:'#3D3F3F'}} placeholder="全部"/>
      <Input style={{position:'absolute',left:'840px',top:'396px',width:'273px',height:'28px',fontSize:'23px',color:'#3B3D3E'}} placeholder="全部"/>
      <Input style={{position:'absolute',left:'367px',top:'432px',width:'291px',height:'27px',fontSize:'22px',color:'#333334'}} placeholder="全部"/>
      <Input style={{position:'absolute',left:'839px',top:'432px',width:'274px',height:'27px',fontSize:'22px',color:'#333434'}} placeholder="全部"/>
      <Input style={{position:'absolute',left:'373px',top:'468px',width:'295px',height:'27px',fontSize:'22px',color:'#3B393C'}} placeholder="全部"/>
      <Input style={{position:'absolute',left:'841px',top:'467px',width:'272px',height:'29px',fontSize:'24px',color:'#393B3B'}} placeholder="全部"/>
      <Input style={{position:'absolute',left:'368px',top:'505px',width:'95px',height:'27px',fontSize:'22px',color:'#6B6B6B'}} placeholder="原市"/>
      <Input style={{position:'absolute',left:'842px',top:'504px',width:'93px',height:'27px',fontSize:'22px',color:'#373738'}} placeholder="原市"/>
      <Input style={{position:'absolute',left:'838px',top:'540px',width:'291px',height:'27px',fontSize:'22px',color:'#3A3938'}} placeholder="全部"/>
      <Input style={{position:'absolute',left:'367px',top:'576px',width:'290px',height:'27px',fontSize:'22px',color:'#363638'}} placeholder="不显示"/>
      <Input style={{position:'absolute',left:'841px',top:'576px',width:'293px',height:'27px',fontSize:'22px',color:'#3A3B3A'}} placeholder="全部"/>
      <Input style={{position:'absolute',left:'365px',top:'611px',width:'294px',height:'29px',fontSize:'24px',color:'#363838'}} placeholder="全部"/>
      <Input style={{position:'absolute',left:'837px',top:'611px',width:'295px',height:'29px',fontSize:'24px',color:'#333537'}} placeholder="全部"/>
      <Input style={{position:'absolute',left:'844px',top:'144px',width:'293px',height:'27px',fontSize:'22px',color:'#000000'}} placeholder=""/>
      <Input style={{position:'absolute',left:'838px',top:'180px',width:'294px',height:'28px',fontSize:'23px',color:'#000000'}} placeholder=""/>
      <Input style={{position:'absolute',left:'372px',top:'216px',width:'268px',height:'27px',fontSize:'22px',color:'#000000'}} placeholder=""/>
      <Input style={{position:'absolute',left:'844px',top:'216px',width:'268px',height:'27px',fontSize:'22px',color:'#000000'}} placeholder=""/>
      <Input style={{position:'absolute',left:'468px',top:'504px',width:'196px',height:'27px',fontSize:'22px',color:'#000000'}} placeholder=""/>
      <Input style={{position:'absolute',left:'941px',top:'504px',width:'195px',height:'28px',fontSize:'23px',color:'#000000'}} placeholder=""/>
      <Input style={{position:'absolute',left:'366px',top:'648px',width:'291px',height:'27px',fontSize:'22px',color:'#000000'}} placeholder=""/>
      <DatePicker bordered={false} style={{position:'absolute',left:'639.0px',top:'202.0px',width:'50px',height:'50px',fontSize:'20px',color:'#000000'}}/>
      <DatePicker bordered={false} style={{position:'absolute',left:'1111.0px',top:'202.0px',width:'50px',height:'50px',fontSize:'20px',color:'#000000'}}/>
      <Select style={{position:'absolute',left:'368px',top:'252px',width:'294px',height:'28px',fontSize:'23px',color:'#5B5C5C'}} placeholder="全部"/>
      <Select style={{position:'absolute',left:'373px',top:'144px',width:'292px',height:'27px',fontSize:'22px',color:'#000000'}} placeholder=""/>
      <Select style={{position:'absolute',left:'372px',top:'180px',width:'294px',height:'28px',fontSize:'23px',color:'#000000'}} placeholder=""/>
    </div>
  );
}
export default App;