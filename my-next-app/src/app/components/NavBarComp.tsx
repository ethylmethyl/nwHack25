import Navbar from 'react-bootstrap/Navbar';

export default function NavBarComp () {
    return (
        <Navbar sticky="top" className="flex bg-white border border-black h-[30%] justify-content-between"> 
            <div className='flex flex-row w-full justify-start'>
                <img 
                    className="justify- align-middle w-10 h-10 pt-2 pl-2 mr-2 ml-5"
                    src="/images/houseLined.png" 
                    alt="House Logo"
                />
                <p className='text-[#272424] text-[29px] text-pretty font-inter font-bold mr-20'>Homi</p>
                <input className='flex pl-3 w-[50%] border-2 border-[#BCACAC] rounded-lg text-[#8E7979] text-[17px] font-inter font-normal max-h-12 mr-80' placeholder='   Enter an address, neighborhood, city, or postal code'></input>
                <div className="flex w-12 h-12 bg-white shadow-lg rounded-full mt-1">
                    <img 
                        className="flex justify-center align-middle w-10 h-10 pt-2 pl-2"
                        src="/images/Frame.svg" 
                        alt="pfp"
                    />
                </div>
            </div>
        </Navbar>
    );
}