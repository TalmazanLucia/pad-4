import cls from './App.module.scss';
import Categories from "./modals/Categories/Categories.tsx";
import Clothes from "./modals/Clothes/Clothes.tsx";
import {useState} from "react";

function App() {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  return (
    <div className={cls.appWrapper}>
      <p>Hainele tale</p>
        <Categories handleSelect={(value) => setSelectedCategory(value)}/>
        <Clothes selectedCategory={selectedCategory}/>
    </div>
  )
}

export default App
