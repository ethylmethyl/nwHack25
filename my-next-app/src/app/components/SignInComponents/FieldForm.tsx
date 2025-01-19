
export const FieldForm = ({label, placeholder}) => {
    return(
        <div className=" flex flex-col justify-start pt-2 max-w-[80%]">
            <div className="text-[16px] text-[#8E7979] font-inter font-normal">{label}</div>
            <input 
                className="flex h-10 pl-1 justify-items-start border-2 border-[#BCACAC] rounded-md text-[#8E7979] text-[14px] font-inter font-normal" 
                placeholder={`  ${placeholder}`}>
            </input>
        </div>
    );
}