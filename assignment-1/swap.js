// 检查 MetaMask 是否安装
if (typeof window.ethereum !== 'undefined') {
    console.log('MetaMask is installed!');
} else {
    alert('Please install MetaMask!');
}
// 用于跟踪钱包是否已连接
let isConnected = false; 

// 隐藏二级菜单
document.getElementById('hiddenBar').hidden = true;
function secondNavBarHide() {
    document.getElementById('hiddenBar').hidden = true;
}
function secondNavBarShow() {
    document.getElementById('hiddenBar').hidden = false;
}

// 按钮调换内容
function reverse()//点击交换按钮运行此处代码
{
    var a=document.getElementById('swapFrom').value;
    document.getElementById('swapFrom').value=document.getElementById('swapTo') .value;
    document.getElementById('swapTo').value=a;
}

// 连接钱包的函数
async function connectWallet() {
    try {
        if (!isConnected) {
            // 请求 MetaMask 的用户授权
            const accounts = await ethereum.request({ method: 'eth_requestAccounts' });

            // 获取用户的第一个以太坊地址
            const account = accounts[0];

            // 显示用户地址
            console.log('Connected account:', account);

            // 更新按钮文本或在页面上显示已连接的地址
            document.getElementById('checkMetaMask').innerText = `Get Quotes`;
            document.getElementById('checkMetaMask-vice').hidden=true;
            document.getElementById('userWallet').innerText = `${account}`;

            isConnected = true; // 标记为已连接
        } else {
            const web3 = new Web3(window.ethereum);
            // 获取连接账户的余额
            const account = document.getElementById('userWallet').innerText.trim();
            console.log('account:', account)
            /* const balanceEth = await ethereum.request({
                method: 'eth_getBalance',
                params: [account, 'latest']
            }); */
            const balanceEth = await web3.eth.getBalance(account);
            // 将余额转换为以太币（ETH）
            console.log('Balance (ETH):', balanceEth);
            const balance = web3.utils.fromWei(balanceEth, 'ether');

            // 获取输入框中的金额，并处理为空的情况
            let amount = parseFloat(document.getElementById('amount').value);
            // 如果 amount 为空或不是一个有效的数字，则将其赋值为默认值 0
            if (isNaN(amount)) {
                amount = 0;
            }
            console.log('Entered Amount:', amount);

            // 比较余额与输入金额
            if (balance >= amount) {
                alert(`You have sufficient balance. your balance is ${balance}`);
                //document.getElementById('getBalance').innerText = `You have sufficient balance. your balance is ${balance}`
            } else {
                //alert(`Insufficient balance. your balance is ${balance}`);
                document.getElementById('getBalance').innerText = `Insufficient balance. your balance is ${balance}`
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// 监听按钮点击事件
document.getElementById('checkMetaMask').addEventListener('click', connectWallet);
document.getElementById('checkMetaMask-vice').addEventListener('click', connectWallet);
// 显示二级菜单
document.addEventListener('click', function(event) {
    // 获取指定区域的元素
    const specifiedElement = document.getElementById('navOverview'); // 替换为你指定区域的ID
    console.log('event:',event.target);
    console.log('elements:',specifiedElement);
    // 判断点击是否在指定区域内
    if (specifiedElement && !specifiedElement.contains(event.target)) {
        // 如果点击不在指定区域内，执行操作，例如隐藏菜单
        secondNavBarHide(); // 调用隐藏二级菜单的函数
    } else {
        // 如果点击在指定区域内，执行其他操作或不做任何处理
        console.log('Clicked inside the specified area');
    }
});